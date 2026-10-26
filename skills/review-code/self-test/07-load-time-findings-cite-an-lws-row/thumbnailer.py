"""Resizes an uploaded image into a thumbnail beside it in the same bucket."""
import io

import boto3
from PIL import Image

S3_THUMBS = boto3.client("s3")


def handler(event, context):
    record = event["Records"][0]["s3"]
    bucket, key = record["bucket"]["name"], record["object"]["key"]
    original = S3_THUMBS.get_object(Bucket=bucket, Key=key)["Body"].read()
    image = Image.open(io.BytesIO(original))
    image.thumbnail((256, 256))
    out = io.BytesIO()
    image.save(out, format="PNG")
    S3_THUMBS.put_object(Bucket=bucket, Key=f"thumbs/{key}", Body=out.getvalue())
