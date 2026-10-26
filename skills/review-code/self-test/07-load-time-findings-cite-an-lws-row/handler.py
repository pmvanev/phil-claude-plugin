"""Lambda entry point for the reports web app's API."""
import json
import os

import boto3
import psycopg

from routing import route_for

S3_CLIENT = boto3.client("s3")
DB = psycopg.connect(os.environ["DATABASE_URL"])


def _check_bucket():
    S3_CLIENT.head_bucket(Bucket=os.environ["REPORTS_BUCKET"])


def _check_database():
    with DB.cursor() as cur:
        cur.execute("SELECT count(*) FROM reports")
        if cur.fetchone()[0] == 0:
            raise RuntimeError("reports table is empty")


def _check_user_pool():
    boto3.client("cognito-idp").describe_user_pool(UserPoolId=os.environ["USER_POOL_ID"])


_check_bucket()
_check_database()
_check_user_pool()


def report_count():
    with DB.cursor() as cur:
        cur.execute("SELECT count(*) FROM reports")
        return cur.fetchone()[0]


def handler(event, context):
    cognito = boto3.client("cognito-idp")
    user = cognito.get_user(AccessToken=event["headers"]["authorization"])
    route = route_for(event["rawPath"])
    if route == "export":
        textract = boto3.client("textract")
        job = textract.start_document_analysis(DocumentLocation=json.loads(event["body"]))
        return {"statusCode": 202, "body": json.dumps({"job": job["JobId"]})}
    if route == "count":
        return {"statusCode": 200, "body": json.dumps({"reports": report_count()})}
    return {"statusCode": 200, "body": json.dumps({"user": user["Username"]})}
