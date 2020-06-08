# Serverless Mini [WIP]

## Table of contents
* Introduction
* Repo content
* Setup
* Issues & Bugs

## Introduction
Using the serverless framework, the puprose is to create a serverless pipeline with 2 lambdas and an RDS. 
The flow is that once a csv file is uploaded to an upload bucket, the first lambda is triggered which moves the csv file to another bucket.
Once the file is put in the new bucket, a second lambda is triggered that transforms the file and loads it into an RDS.

## What is included in the repo:

- **serverless.yml**: This is the config file that configures all the bits and pieces needed. Using this file, the serverless framework creates 2 S3 buckets, a postgresql RDS and 2 lambda functions based on the extract and transform functions.
- **extract.py**: This is the first lambda function, it moves csv file from a bucket to another. It is not really extracting the data from a csv just moving files around.
- **transform.py**: [WIP] bigtime.  This is triggered when the csv is moved to a newfile. Manipulates the file and saves it into an RDS (Implementation incomplete).
- **requirements.txt**: Requirements for the handlers. The requirements is zipped through the serverless python-requirements plugin.


## Setup:
- Install the serverless framework at: www.serverless.com
- After cloning the repo, do `$serverless`. This will take you through the steps of setting up your AWS credentials and choosing the repo/project for deployment.
- Make sure that the user permissions are set to AdminAccess in AWS. You can create a group as well and add user to the group with permissions set in the group. 
- run `$sls deploy`to deploy. This will create all the resources and lambdas required.

## Issues & Bugs:
- Although the events for the lambda functions are set in the yaml file, the triggers are not showing in AWS. There could be an issue in how the events are set in the yml file. 
These could be set by going to the lambdas function, clicking on triggers, selecting the upload bucket from S3 from the events, and Put as an action for both lambdas.
- Python requirements should be zipped when dealing with large packages. Although there are no issues importing boto3, I was getting an error with pandas. This is likely appearing when unzipping requirements. To avoid that make sure to add the try import command as instructed in the python-requirements.
- There is still an issue when importing pandas caused by numpy ( a dependency of pandas). The error is found in a text file called transform_lambda_error. This is generated when running a payload test on the transform lambda.
- I am using python libs for transformation which could be 'too much' given the size limits of lambdas. Adding SQLaclhemy for example to use its engine to load the dataframe into RDS was causing failure when deploying. This is due to the large file size of requiremens even after zipping them.
- Note that the transform lambda is far from complete due to the issues mentioned above. 



