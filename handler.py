"""
Handlers for the S3 events defined under functions in the
Serverless.yml file.
Events are passed automatically noramlly as Dict object with
Key value structure. Refer to:
https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html

for information on the context refer to:
https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
"""

import json
import boto3
import os


def extract(event, context):
    """
    Extract a csv file when uploaded to
    bucket and save raw data in a new one.
    Args:
        event(Dict): S3 event based on the triggers in the serverless.yml
        context(obj): context object when lambda runs.
    """
    print('what is going on')
    print(event)
    dst_bucket = os.environ['S3_DST_BUCKET']
    s3 = boto3.resource('s3')
    s3_event = event['Records'][0]['s3']

    src_bucket = s3_event['bucket']['name']
    src_file = s3_event['object']['key']

    copy_source = {
      'Bucket': src_bucket,
      'Key': src_file
    }
    dst_bucket = s3.Bucket(dst_bucket)
    dst_bucket.copy(copy_source, f'raw/input/{src_file}')


def trasnform_load(even, context):
    """Transfrom the data obtained after the extract and load it into a DB."""
    pass
