import uuid
import os
import boto3
import boto
from boto.s3.key import Key
import botocore
from boto3.s3.transfer import TransferConfig
from excel2json import convert_from_file

from flask import Flask, request

app = Flask(__name__)

@app.route("/<variable>", methods=['GET', 'POST'])
def home(variable):
    bucket_name = 'my-dump-files'
    if variable == 'upload':
        s3 = boto.connect_s3()
        bucket = s3.get_bucket(bucket_name)
        k = Key(bucket)
        data_file = request.files.get('myfile')
        contents = data_file.read()
        k.key = str(uuid.uuid4())
        k.set_contents_from_string(contents)
        return '<a href="/'+k.key+'">http://127.0.0.1:5000/'+k.key+'</a>'

    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(variable,'downloads/'+variable+'.xlsx')
    convert_from_file('downloads/'+variable+'.xlsx', 'json-files')
    return 'Copy and paste in your browser:<h4>file:///'+ os.path.dirname(os.path.abspath(__file__))+'/json-files/Sheet1.json</h4>'