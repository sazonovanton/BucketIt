# BucketIt

BucketIt is a command line interface (CLI) tool that simplifies uploading files to S3 bucket. It can be used for uploading a single file, multiple files in a directory, or all files in a directory recursively.

## Prerequisites

* Python 3
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* An S3 account with credentials

## Installation

Through PyPI:
```
pip3 install bucketit
```

You can create a `.bucketit_config` file by running script once or creating it in your home directory (`C:\Users\username\.bucketit_config` on Windows, `/home/username/.bucketit_config` on Linux) using `bucketit_config.example` file. 

**IMPORTANT**: Access key and secret key stored in configuration file in your home directory as a plain text. I plan to change config storage to environment variables or some other secure way in the future.

## Configuration

BucketIt requires a configuration file to run. The configuration file should be in [INI file format](https://en.wikipedia.org/wiki/INI_file) and should contain the following fields:

```
[S3]
endpoint_url = <endpoint_url>
access_key = <access_key>
secret_key = <secret_key>
bucket_default = <bucket_default>
```
* `endpoint_url` - The endpoint URL for your S3 service.
* `access_key` - Your S3 access key.
* `secret_key` - Your S3 secret key.
* `bucket_default` - (Optional) The default bucket to use for uploads. If not specified, you will be prompted for the bucket name when you run BucketIt.

If the configuration file does not exist or cannot be read, BucketIt will prompt you to create a new configuration file.
*WARNING: Access key and secret key stored in configuration file as a plain text.*

## Usage

```
usage: bucketit [-h] [--filename FILENAME] [--date] [--folder FOLDER] [-r] [-b BUCKET] [-v] [--version] [--nofolder] file

BucketIt is a simple tool for uploading files to S3. 
See README for more details.

positional arguments:
  file                  Path to the file you want to upload

optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME   Filename to use in the bucket. If not specified, the original filename will be used
  --date                Add date in a format of YYYY/MM/DD before the filename in bucket
  --folder FOLDER       Folder to upload the file to. If not specified, the file will be uploaded to the root of the bucket
  -r, --recursive       Upload all files in the directory recursively
  -b BUCKET, --bucket BUCKET
                        Bucket name to upload the file to. If not specified, the default bucket will be used
  -v, --verbose         Verbose output
  --version             Tool version
  --nofolder            Do not create a folder with the same name as the folder with files if recursive is set
```

To upload a file to an S3 bucket, run the following command:
```
bucketit path/to/file
```
You can specify the following options:
* `--filename` - Filename to use in the bucket. If not specified, the original filename will be used.
* `--date` - Add date in a format of YYYY/MM/DD before the filename in bucket.
* `--folder` - Folder to upload the file to. If not specified, the file will be uploaded to the root of the bucket.
* `-r` or `--recursive` - Upload all files in the directory recursively.
* `--nofolder` - Do not create a folder with the same name as the folder with files if recursive is set.
* `-b` or `--bucket` - Bucket name to upload the file to. If not specified, the default bucket will be used.
* `-v` or `--verbose` - Verbose output.
* `-s` or `--silent` - Silent - no output.

By default, the file will be uploaded to the default bucket specified in the configuration file. If no default bucket is specified, you will be prompted for the bucket name when you run BucketIt.

You can also use the `--date` option to enable adding the current date to the filename in the bucket. This is useful if you want to keep a history of your files. For example, if you run the following command:
```
bucketit path/to/file --date
```
The file will be uploaded to the bucket with the following filename:
```
2020/01/01/file
```
Also progress bar will be shown during upload. Verbose output will have more information about the upload process (speed, upload time, destination). Silent output will have no output at all.

