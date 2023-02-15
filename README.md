# BucketIt

BucketIt is a simple command line interface (CLI) tool for uploading files to an S3 bucket. This tool uses the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library to communicate with S3.
Installation

To install the dependencies for BucketIt, run the following command:
```
pip install -r requirements.txt
```

## Configuration

BucketIt requires a configuration file to run. The configuration file should be in [INI file format](https://en.wikipedia.org/wiki/INI_file) and should contain the following fields:

```
[S3]
endpoint_url = <endpoint_url>
access_key = <access_key>
secret_key = <secret_key>
bucket_default = <bucket_default>

    endpoint_url - The endpoint URL for your S3 service.
    access_key - Your AWS access key.
    secret_key - Your AWS secret key.
    bucket_default - (Optional) The default bucket to use for uploads. If not specified, you will be prompted for the bucket name when you run BucketIt.
```

If the configuration file does not exist or cannot be read, BucketIt will prompt you to create a new configuration file.

## Usage

```
usage: bucketit [-h] [--nodate] [-b BUCKET] [-v] file

BucketIt is a simple tool to upload files to S3. Config file is required. See README for more details.

positional arguments:
  file           Path to the file you want to upload

optional arguments:
  -h, --help     show this help message and exit
  --nodate       Do not add date in a format of YYYY/MM/DD before the filename in bucket
  -b BUCKET      Bucket name to upload the file to. If not specified, the default bucket will be used
  -v, --verbose  Verbose output
```

To upload a file to an S3 bucket, run the following command:
```
bucketit <file> --bucket <bucket>
```
* `<file>` - The path to the file you want to upload.<br>
* `<bucket>` - The name of the S3 bucket you want to upload the file to.


By default, the file will be uploaded to the default bucket specified in the configuration file. If no default bucket is specified, you will be prompted for the bucket name when you run BucketIt.

You can also use the `--nodate` option to disable adding the current date to the filename in the bucket. This can be useful if you want to overwrite an existing file with the same name.


_Thanks to [ChatGPT](https://chat.openai.com/chat/) for helping with this description :)_