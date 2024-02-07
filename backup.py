#
# backup -- p3. css436
# Author: Yasmine Subbagh
#

import sys
import boto3


if(len(sys.argv) != 2):
    sys.exit("Error: Improper arguemnts passed.")

#connect to s3
session = boto3.Session(profile_name='dev')
client = boto3.client('s3')

