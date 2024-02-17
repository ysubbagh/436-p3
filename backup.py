#
# backup -- p3. css436
# Author: Yasmine Subbagh
#

import sys
import boto3
import os
from datetime import datetime

#check if the bucket exists
def check_bucket_exists(bucket_name):
    client = boto3.client('s3')
    response = client.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == bucket_name:
            return True
    return False

#check to see if it is a empty direcotry, true is empty
def is_directory_empty(directory_path):
    content = os.listdir(directory_path)
    return len(content) == 0

#recursivly backup to aws
def backup(local_path, bucket_name, cloud_path):
    #connect to s3 (AWS)
    client = boto3.client('s3')
    #get credientials 
    region = client.meta.region_name
    location = {'LocationConstraint': region}

    #check to see if bucket exists, if not, create
    if not check_bucket_exists(bucket_name):
        client.create_bucket(Bucket = bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket {bucket_name} created")
    
    client.head_bucket(Bucket = bucket_name)
    print(f"Backing up to {bucket_name}")

    #upload files
    for (root, dirs, files) in os.walk(local_path):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            if is_directory_empty(dir_path):
                cloud_dir_path = os.walk.join(cloud_path, os.path.relpath(dir_path, local_path))
                empty_file_path = '.empty'  # Hidden file name
                client.put_object(Bucket=bucket_name, Key=os.path.join(cloud_path, empty_file_path), Body=b'')

        for file in files:
            if file == '.DS_Store':
                continue
            #get path and cloud path key
            file_path = os.path.join(root, file)
            cloud_key = os.path.join(cloud_path, os.path.relpath(file_path, local_path))

            #get last modified time to ensure no duplicate copying
            local_mod_date = datetime.fromtimestamp(os.path.getmtime(file_path))

            #see if item already exists
            try:
                item = client.head_object(Bucket = bucket_name, Key = cloud_key)
                cloud_mod_date = item['LastModified'].replace(tzinfo = None)
            except client.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    pass    
                else:
                    raise

            client.upload_file(file_path, bucket_name, cloud_key)
            print(f"Uploaded {file_path}")
            
    
#main function to initiate/call the backup
def main():
    args = sys.argv
    #check arguemtns length is correct
    if(len(args) != 3):
        sys.exit("Error: Improper arguemnts passed.")

    #parse variables from arguemnts
    local_path = args[1]
    args = args[2].split('::')
    bucket_path = args[0]
    cloud_path = args[1]

    #check for empty arguemnts
    if(local_path == "" or bucket_path == "" or cloud_path == ""):  
        sys.exit("Error: Improper arguemnts passed.")

    #send to restore function
    backup(local_path, bucket_path, cloud_path)

#start from main
if __name__ == "__main__":
    main()