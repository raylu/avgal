#!/usr/bin/env python3

import argparse
import json
import pathlib

import boto3
import rtoml

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--dst', required=True, help='dir in the bucket to upload to')
	args = parser.parse_args()
	print(args)

	config = rtoml.load(pathlib.Path('config.toml'))
	print(config)

	bucket_conf = config['bucket']
	s3 = boto3.resource('s3', endpoint_url=bucket_conf['endpoint'],
		aws_access_key_id=bucket_conf['access_key_id'], aws_secret_access_key=bucket_conf['secret_access_key'])
	bucket = s3.Bucket(bucket_conf['bucket'])
	files_obj = bucket.Object(args.dst + '/files.json')
	files = json.load(files_obj.get()['Body'])
	print(files)

if __name__ == '__main__':
	main()
