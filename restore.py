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
    local_path = args[1]
    args = args[0].split('::')
    bucket_path = args[0]
    cloud_path = [1]

    #check for empty arguemnts
    if(local_path == "" or bucket_path == "" or cloud_path == ""):  
        sys.exit("Error: Improper arguemnts passed.")



#recursivly backup to aws
def restore():
    #connect to s3
    client = boto3.client('s3')


