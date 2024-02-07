#
# backup -- p3. css436
# Author: Yasmine Subbagh
#

import sys
import boto3
import os


def main():
    args = sys.argv
    #check arguemtns length is correct
    if(len(args) != 2):
        sys.exit("Error: Improper arguemnts passed.")

    #parse string from arguemnts
    args = args.split(' ')
    local_path = args[0]
    args = args[1].split('::')
    bucket_path = args[0]
    cloud_path = [1]

    #check for empty arguemnts
    if(local_path == "" or bucket_path == "" or cloud_path == ""):  
        sys.exit("Error: Improper arguemnts passed.")

    #print paths
    print(f"local path: {local_path}")
    print(f"bucket: {bucket_path}")
    print(f"cloud path: {cloud_path}")



#recursivly backup to aws
def backup(local_path, bucket_name, cloud_path):
    #connect to s3
    client = boto3.client('s3')

    #check to see if bucket exists, create if not
    try:
        resp = client.head_bucket(Bucket = bucket_name)
    except client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404': #if bucket doesnt already exist, create it
            try:
                create = client.create_bucket(Bucket = bucket_name)
            except Exception as e:
                sys.exit("Error: Couldn't create bucket.")
    

