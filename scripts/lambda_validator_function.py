import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Fixed for Prototype Testing
    bucket = 'prashant-aws-learning-2026'
    data_file = 'landing/NVS_LEAP_CASE_20260206.txt'
    ctl_file = 'landing/NVS_LEAP_CASE_20260206.ctl'
    
    try:
        # 1. Read Control File (Format: FileName|RowCount|Timestamp)
        ctl_obj = s3.get_object(Bucket=bucket, Key=ctl_file)
        ctl_content = ctl_obj['Body'].read().decode('utf-8').strip()
        expected_count = int(ctl_content.split('|')[1])
        
        # 2. Check Data File Row Count
        data_obj = s3.get_object(Bucket=bucket, Key=data_file)
        data_content = data_obj['Body'].read().decode('utf-8').splitlines()
        actual_count = len(data_content)-1
        
        if actual_count == expected_count:
            res = f"✅ SUCCESS: Row count matches ({actual_count})."
            print(res)
            return {"status": "SUCCESS", "details": res}
        else:
            res = f"❌ FAILED: Expected {expected_count}, found {actual_count}."
            print(res)
            return {"status": "FAILED", "details": res}
            
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
