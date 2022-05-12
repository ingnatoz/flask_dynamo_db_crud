# https://github.com/irtiza07/s3-boto3-tutorial/blob/master/s3_tutorial.py
from flask import Blueprint, jsonify, request
import boto3
import requests
import json
import os
import config

bucket_r = Blueprint("Bucket-Route", __name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.REGION_NAME
)


# Create Bucket
@bucket_r.route('/create_bucket', methods=['POST'])
def create_bucket():
    data = request.get_json()
    s3.create_bucket(Bucket=data['bucket_name'])
    result = {'msg': 'Add bucket successful'}
    return jsonify(result), 200


# List all buckets
@bucket_r.route('/list_buckets', methods=['GET'])
def get_list_buckets():
    buckets_resp = s3.list_buckets()
    buckets = []
    for bucket in buckets_resp["Buckets"]:
        buckets.append(bucket)
    return jsonify(buckets), 200


# List all objects in a bucket
@bucket_r.route('/list_all_objects', methods=['POST'])
def list_all_objects():
    data = request.get_json()
    response = s3.list_objects_v2(Bucket=data['bucket_name'])
    contents = []
    for obj in response["Contents"]:
        contents.append(obj)
    return jsonify(contents), 200


# Upload file to bucket
@bucket_r.route('/get_users', methods=['GET'])
def get_users():
    url = 'https://jsonplaceholder.typicode.com/users'  # petition example
    headers = {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response = response.json()
        bucket_name = "bucket_name"
        for user in response:
            folder = "data/"
            file_name = str(user['id']) + ".json"
            with open(folder + file_name, 'w') as f:
                json.dump(user, f)
            with open(folder + file_name, "rb") as f:
                print(f.name)
                s3.upload_fileobj(f, bucket_name, folder + file_name)
                # os.remove(file_id) # delete files .json
        result = {'msg': 'resources created'}
        return jsonify(result), 200
    result = {'msg': 'Some error occurred'}
    return jsonify(result), 500


# Download File
@bucket_r.route('/download_file', methods=['POST'])
def download_file():
    data = request.get_json()
    folder = data['folder']
    file_name = str(data['id']) + ".json"
    bucket_name = data['bucket_name']
    s3.download_file(bucket_name, folder + file_name, folder + "downloaded_file" + file_name)
    result = {'msg': 'downloaded file ' + file_name}
    return jsonify(result), 200


@bucket_r.app_errorhandler(404)
def handle_404(err):
    result = {'error': '404'}
    return jsonify(result), 404


@bucket_r.app_errorhandler(500)
def handle_500(err):
    result = {'error': '500'}
    return jsonify(result), 500
