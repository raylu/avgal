#!/usr/bin/env python3

import argparse
import dataclasses
import io
import json
import pathlib
import typing

import boto3
import rtoml

def main() -> None:
	parser = argparse.ArgumentParser()
	parser.add_argument('--dst', required=True, help='dir in the bucket to upload to')
	parser.add_argument('paths', nargs='+', type=pathlib.Path, help='file paths or directory to upload')
	args = Args(**vars(parser.parse_args()))
	paths = resolve_paths(args.paths)

	config = rtoml.load(pathlib.Path('config.toml'))

	bucket_conf = config['bucket']
	s3 = boto3.resource('s3', endpoint_url=bucket_conf['endpoint'],
		aws_access_key_id=bucket_conf['access_key_id'], aws_secret_access_key=bucket_conf['secret_access_key'])
	bucket = s3.Bucket(bucket_conf['bucket'])
	files_obj = bucket.Object(args.dst + '/files.json')
	files: list[str] = json.load(files_obj.get()['Body'])
	print(f'got {files_obj.key} with {len(files)} files')

	for p in paths:
		print(f'uploading to {args.dst}/{p.name}')
		bucket.Object(f'{args.dst}/{p.name}').upload_file(str(p))
		thumb_path = p.parent / f'{p.stem}-thumb{p.suffix}'
		bucket.Object(f'{args.dst}/{thumb_path.name}').upload_file(str(thumb_path))
		files.append(p.name)
	
	files.sort()
	print(f'updating {files_obj.key} with {len(files)} files')
	files_obj.upload_fileobj(io.BytesIO(json.dumps(files).encode('utf-8')))

def resolve_paths(paths: typing.Sequence[pathlib.Path]) -> typing.Sequence[pathlib.Path]:
	if len(paths) == 1 and paths[0].is_dir():
		paths = [p for p in paths[0].glob('*.avif') if not p.name.endswith('-thumb.avif')]
	assert all(p.suffix == '.avif' for p in paths)
	assert all(p.exists() for p in paths)
	assert all((p.parent / f'{p.stem}-thumb{p.suffix}').exists() for p in paths)
	return paths

@dataclasses.dataclass
class Args:
	dst: str
	paths: list[pathlib.Path]

if __name__ == '__main__':
	main()
