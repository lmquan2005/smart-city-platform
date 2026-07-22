import boto3
from botocore.exceptions import ClientError
from config.logger import logging
from config.config import S3_BUCKET, AWS_REGION

s3 = boto3.client("s3", region_name=AWS_REGION)


def upload_file(local_path, object_name):
    try:
        s3.upload_file(
            local_path,
            S3_BUCKET,
            object_name
        )

        logging.info(
            f"Uploaded {local_path} -> s3://{S3_BUCKET}/{object_name}"
        )

        return True

    except ClientError as e:
        logging.error(e)
        return False