"""The ledger API, behind a Function URL; SnapStart restores it from a snapshot."""
import uuid

import boto3

LEDGER = boto3.client("s3")
INSTANCE_ID = str(uuid.uuid4())


def handler(event, context):
    body = LEDGER.get_object(Bucket="ledger", Key=event["rawPath"].lstrip("/"))["Body"].read()
    return {"statusCode": 200, "headers": {"X-Instance": INSTANCE_ID}, "body": body.decode()}
