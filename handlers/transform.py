"""
Handlers for the S3 events defined under functions in the
Serverless.yml file.
Events are passed automatically noramlly as Dict object with
Key value structure. Refer to:
https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html

for information on the context refer to:
https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
"""

# As recommended by the python-requirements plugin. See:
# Dealing with Lambda's limitation at
# https://github.com/UnitedIncome/serverless-python-requirements
try:
    import unzip_requirements
except ImportError:
    pass

import boto3
import pandas as pd


def transform_load(event, context):

    """Transfrom the data obtained after the extract and load it into a DB."""
    s3 = boto3.resource('s3')
    s3_event = event['Records'][0]['s3']

    # Source is the raw data in this case.
    src_bucket = s3_event['bucket']['name']
    src_file = s3_event['object']['key']
    s3 = boto3.client('s3')
    s3_obj = s3.get_object(Bucket=src_bucket, Key=src_file)
    df = pd.read_csv(s3_obj)

    # Update MovementDateTime to iso format,
    # the assumption is that there are no missing values.
    df['MovementDateTime'] = pd.to_datetime(
        df['MovementDateTime'], format='%Y-%m-%d %H:%M:%S'
        )
    df['BeamRatio'] = df['Beam']/df['Length']

    # create engine to connect to RDS postgres using sqlaclhemy engine.
    # engine = create_engine(create_engine('postgresql://user:password@host/database'))
    # engine.execute("""Row SQL to create a table with required columns""")
    # Read csv to a pandas df
    # df.to_sql('table_name', con=engine)
