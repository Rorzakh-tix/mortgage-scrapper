import boto3
from botocore.client import Config

from library.minio_aws.minio_config import AWS_ACCESS, AWS_SECRET

s3 = boto3.resource('s3',
                    endpoint_url='https://0trs2u.stackhero-network.com',
                    aws_access_key_id=AWS_ACCESS,
                    aws_secret_access_key=AWS_SECRET,
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1',
                    )


async def create_bucket(bucket_name: str):
    s3.create_bucket(Bucket=bucket_name)


async def upload_file_to_s3(filepath: str, bucket_name: str, filename: str):
    s3.Bucket(bucket_name).upload_file(filepath, filename)


async def download_file_from_s3(bucket_name: str, filename: str, filepath: str):
    s3.Bucket(bucket_name).download_file(filename, filepath)
