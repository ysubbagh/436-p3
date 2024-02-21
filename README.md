<!> 
<1> must install boto3
<2> must ensure pip version with boto and version of python being run are the same
<3> was locally tested and ran on python3 version 10.6

to compile and run restore ->
python3 restore.py bucket-name::directory-name directory-name

to compile and run backup ->
python3 backup.py directory-name bucket-name::directory-name
