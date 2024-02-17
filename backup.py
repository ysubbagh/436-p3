#
# backup -- p3. css436
# Author: Yasmine Subbagh
#

import sys
import boto3
import os
from datetime import datetime

#recursivly backup to aws
def backup(local_path, bucket_name, cloud_path):
    #connect to s3 (AWS)
    client = boto3.client('s3')

    #check to see if bucket exists, create if not
    try:
        resp = client.head_bucket(Bucket = bucket_name)
        print(f"Backing up to {bucket_name}")
    except client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404': #if bucket doesnt already exist, create it
            try:
                create = client.create_bucket(Bucket = bucket_name)
                print(f"bucket {bucket_name} created")
            except Exception as e:
                sys.exit("Error: Couldn't create/access bucket.")

    #upload files
    for (root, dirs, files) in os.walk(local_path):
        for file in files:
            #get path and cloud path key
            file_path = os.path.join(root, file)
            cloud_key = file_path[len(local_path) + 1:]

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


    

