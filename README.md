# 📜 CloudTrailinguist

**CloudTrailinguist** is a lightweight forensic Python tool designed to stream and filter AWS CloudTrail logs directly from S3. 🕵️‍♂️ Instead of downloading gigabytes of logs to your local machine, this script decompresses and analyzes the stream in memory to identify infrastructure **mutations** (non-read-only events) in real-time. ⚡

## 🚀 Key Features
* **☁️ Zero Footprint:** Streams `json.gz` archives directly from S3 using `boto3`. No local storage is required.
* **🔍 Forensic Filtering:** Automatically ignores "ReadOnly" events to focus exclusively on mutations (Create, Delete, Update).
* **📅 Automated Pathing:** Dynamically calculates the S3 log path based on the current UTC date.

## 🛠️ Quick Start

### 1. Prerequisites
* 🐍 Python 3.x
* 📦 `boto3` library: `pip install boto3`
* 📑 An active AWS CloudTrail delivering logs to an S3 bucket.

### 2. Configuration
Create a `configtrail.json` file in the root directory (you can use the placeholder file as a template):

```json
{
    "cloudtrail": {
        "name": "YOUR_TRAIL_NAME",
        "account_id": "000000000000",
        "region": "us-east-1"
    },
    "s3": {
        "bucket": "YOUR_AUDIT_LOG_BUCKET"
    },
    "kms": {
        "description": "YOUR_KEY_DESCRIPTION",
        "alias": "alias/YOUR_KEY_ALIAS"
    }
}
```

### 3. Usage 💻

Simply run the script. It will begin streaming and printing any mutation events found for the current day:
```Bash

python main.py
```

🔐 Security Best Practices

For maximum security, do not use hardcoded Access Keys. 🚫

If running from an EC2 instance, it is recommended to attach an IAM Role to the instance with the AmazonS3ReadOnlyAccess policy. The script will automatically detect and use these credentials via the Instance Metadata Service. 🛡️
