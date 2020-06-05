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


def extract(event, context):
    """
    Extract a csv file when uploaded to
    bucket and save raw data in a new one.
    Args:
        event(Dict): S3 event based on the triggers in the serverless.yml
        context(obj): context object when lambda runs.
    """
    print('what is going on')
    s3 = boto3.resource('s3')
    event_records_string = event['Records'][0]['body']
    event_records_dict = json.loads(event_records_string)

    src_bucket_name = event_records_dict['Records'][0]['s3']['bucaket']['name']
    src_file_name = event_records_dict['Records'][0]['s3']['object']['key']

    copy_source = {
      'Bucket': src_bucket_name,
      'Key': src_file_name
    }
    dst_bucket = s3.Bucket('data-rio-1984')
    dst_bucket.copy(copy_source, f'raw/input/{src_file_name}')


def trasnform_load(even, context):
    """Transfrom the data obtained after the extract and load it into a DB."""
    pass
