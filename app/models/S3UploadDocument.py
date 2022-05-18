import boto3
import requests
from io import BytesIO
from urllib.request import urlopen
import os
from boto3.s3.transfer import TransferConfig

def UploadDocumentS3(file, bucket, key, request_data):
    s3= boto3.client(
        service_name = 's3',
        region_name = 'us-east-2',
        aws_access_key_id = 'AKSJJHKBKASJUCGSANK',
        aws_secret_access_key='JHSHFLJSFLHO7472369R8WHFJKS'
    )
    UPLOAD_FOLDER = './Temp/'

    file.save(UPLOAD_FOLDER + file.filename)
    request_data["filesize"] = os.path.getsize(UPLOAD_FOLDER + file.filename)
    s3.upload_file(UPLOAD_FOLDER + file.filename, bucket, key + "/" + file.filename)
    os.remove(UPLOAD_FOLDER + file.filename)