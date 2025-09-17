import boto3
import pandas as pd
import os

def ingest_from_s3(bucket_name, file_key, aws_access_key, aws_secret_key, save_dir):
    """Download CSV from S3 and save locally."""
    os.makedirs(save_dir, exist_ok=True)
    s3 = boto3.client(
        "s3", 
        aws_access_key_id=aws_access_key, 
        aws_secret_access_key=aws_secret_key
    )
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(obj['Body'])
    raw_path = os.path.join(save_dir, "raw_data.csv")
    df.to_csv(raw_path, index=False)
    print(f"Raw data saved at {raw_path}")
    return raw_path
