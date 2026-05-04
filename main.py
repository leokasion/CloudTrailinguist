import boto3
import gzip
import json
import io
import sys
from datetime import datetime, timezone

def load_config(filepath='configtrail.json'):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL_ERROR: {filepath} not found.", file=sys.stderr)
        sys.exit(1)

def get_dynamic_prefix(account_id, region):
    """Generates the CloudTrail S3 path based on current UTC date."""
    now = datetime.now(timezone.utc)
    date_path = now.strftime('%Y/%m/%d')
    return f"AWSLogs/{account_id}/CloudTrail/{region}/{date_path}/"

def cloudtrail_stream(bucket, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    
    try:
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                if not obj['Key'].endswith('.json.gz'):
                    continue
                
                resp = s3.get_object(Bucket=bucket, Key=obj['Key'])
                with gzip.GzipFile(fileobj=io.BytesIO(resp['Body'].read())) as gf:
                    data = json.load(gf)
                    for record in data.get('Records', []):
                        yield record
    except Exception as e:
        print(f"STREAM_ERROR: {str(e)}", file=sys.stderr)

def main():
    # 1. Load Configuration
    config = load_config()
    
    # 2. Extract Variables
    bucket_name = config['s3']['bucket']
    account_id = config['cloudtrail']['account_id']
    region = config['cloudtrail']['region']
    
    # 3. Generate Dynamic Prefix
    prefix = get_dynamic_prefix(account_id, region)
    
    print(f"--- STREAMING LOGS FOR: {prefix} ---")
    
    for record in cloudtrail_stream(bucket_name, prefix):
        if record.get('readOnly') is False:
            timestamp = record.get('eventTime')
            event = record.get('eventName')
            user = record.get('userIdentity', {}).get('userName', 'system-service')
            src_ip = record.get('sourceIPAddress', '0.0.0.0')
            
            print(f"[*] MUTATION: [{timestamp}] | {src_ip} | {user} | {event}")

if __name__ == "__main__":
    main()