#
# restore -- p3. css436
# Author: Yasmine Subbagh
#

import sys
import boto3
import os

#check if the bucket exists
def check_bucket_exists(bucket_name):
    client = boto3.client('s3')
    response = client.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == bucket_name:
            return True
    return False

#restore from aws to local computer
def restore(local_path, bucket_name, cloud_path):
    #connect to s3
    client = boto3.client('s3')

    #check to see if bucket exists, if not, create
    if not check_bucket_exists(bucket_name):
        print(f"Bucket {bucket_name} does not exist.")
        return

    response = client.list_objects_v2(Bucket = bucket_name, Prefix = cloud_path)

    #test parsing
    print(f"local path: {local_path}")
    print(f"bucket name: {bucket_name}")
    print(f"cloud path: {cloud_path}")


def main():
    args = sys.argv
    #check arguemtns length is correct
    if(len(args) != 3):
        sys.exit("Error: Improper arguemnts passed.")

    #parse variables from arguemnts
    local_path = args[2]
    args = args[1].split('::')
    bucket_path = args[0]
    cloud_path = args[1]

    #check for empty arguemnts
    if(local_path == "" or bucket_path == "" or cloud_path == ""):  
        sys.exit("Error: Improper arguemnts passed.")

    #send to restore function
    restore(local_path, bucket_path, cloud_path)

#start from main
if __name__ == "__main__":
    main()

