import configparser
import boto3
from datetime import datetime
import argparse


class BucketIt:
    def __init__(self, configpath='.config'):
        '''
        Initialize the class. 
        '''
        try:
            self.endpoint_url, self.access_key, self.secret_key, self.bucket_default = self.get_config(configpath)
        except:
            self.no_config(configpath)
        
        self.s3 = boto3.client('s3',
                  endpoint_url=self.endpoint_url,
                  aws_access_key_id=self.access_key,
                  aws_secret_access_key=self.secret_key)
        

    def get_config(self, configpath):
        '''
        Get the config file
        '''
        config = configparser.ConfigParser()
        config.read(configpath)
        endpoint_url = config.get("S3", "endpoint_url")
        access_key = config.get("S3", "access_key")
        secret_key = config.get("S3", "secret_key")
        bucket_default = config.get("S3", "bucket_default") if config.has_option("S3", "bucket_default") else None
        return endpoint_url, access_key, secret_key, bucket_default

    def no_config(self, configpath):
        '''
        Create config from user input if config file does not exist or something went wrong with reading it.
        '''
        print("Config file '{}' does not exist or is not readable. Let's create it.".format(configpath))
        print("Please enter your S3 credentials.")
        endpoint_url = input("Endpoint URL: ")
        access_key = input("Access key: ")
        secret_key = input("Secret key: ")
        bucket_default = input("Default bucket (optional - press Enter to pass): ")
        if bucket_default == '':
            bucket_default = None
        config = configparser.ConfigParser()
        if bucket_default is None:
            config['S3'] = {'endpoint_url': endpoint_url,
                            'access_key': access_key,
                            'secret_key': secret_key}
        else:
            config['S3'] = {'endpoint_url': endpoint_url,
                            'access_key': access_key,
                            'secret_key': secret_key,
                            'bucket_default': bucket_default}
        with open(configpath, 'w') as configfile:
            config.write(configfile)
        print("\nConfig file created. Please run the script again.")
        exit()

    def parse_options(self):
        '''
        Parse command line options. 
        '''
        # add description if help is called
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                            description='BucketIt is a simple tool for uploading files to S3. \nSee README for more details. \nGithub: https://github.com/sazonovanton/BucketIt',
                                            epilog='Usage: bucketit file.txt --bucket mybucket') 
        parser.add_argument("file", help="Path to the file you want to upload", type=str)
        parser.add_argument('--nodate', action='store_true', help='Do not add date in a format of YYYY/MM/DD before the filename in bucket')
        parser.add_argument('-b', '--bucket', default=self.bucket_default, help='Bucket name to upload the file to. If not specified, the default bucket will be used')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')    
        args = parser.parse_args()
        return args

    def upload(self, args):
        '''
        Main function. Uploads the file to the bucket. 
        '''
        filepath = args.file
        nodate = args.nodate
        bucket = args.bucket
        verbose = args.verbose

        if bucket is None:
            print("Please specify the bucket name or set the default bucket in the config file")
            return

        filename = filepath.split('/')[-1]
        now = datetime.now().strftime('%Y/%m/%d/') if not nodate else ''
        s3path = now + filename

        self.s3.upload_file(filepath, bucket, s3path)
        
        if verbose:
            print("File {} uploaded to bucket '{}' as {}".format(filepath, bucket, s3path))


if __name__ == "__main__":
    try:
        b = BucketIt()
        args = b.parse_options()
        b.upload(args)
    except Exception as e:
        print("Something went wrong: {}".format(e))