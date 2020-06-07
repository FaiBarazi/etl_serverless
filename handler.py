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
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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
    s3 = boto3.resource('s3')
    s3_event = event['Records'][0]['s3']

    # Source is the raw data in this case.
    src_bucket = s3_event['bucket']['name']
    src_file = s3_event['object']['key']

    # create engine to connect to RDS postgres
    engine = create_engine(create_engine('postgresql://user:password@host/database'))
    # Read csv to a pandas df
    df = pd.read_csv(f'{path_to_csv}')

    # Do dataframe manipulation here
    # 1: Time to iso fromat
    # 2: For each ship grouped by CallSign,
    #    if the MoveStatus is Under way using engine, fill in any missing or zero speeds with the average of all speeds for that CallSign
    # 3: Create a new feature called BeamRatio calculated as Beam / Length (Beam divided by Length)

    # We can do this or do engine.execute("""SQL command""")
    with engine.connect() as con:
        # Create table of it doesn't exist and drop
        statement = text("""SQL statement""")
        con.execute(statement, *params)

    # Note that pandas Dataframe to_sql takes either an SQLaclhemy engine or sqlite.
    df.to_sql('table_name', con=engine)












