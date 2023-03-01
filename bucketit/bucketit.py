#!/usr/bin/env python3

import configparser
import boto3
from datetime import datetime
import argparse
import os
import logging


class BucketIt:
    def __init__(self):
        '''
        Initialize the class. 
        '''
        # check if config file exists
        homepath = os.path.expanduser("~")
        configpath = os.path.join(f"{homepath}/.bucketit_config")
        if not os.path.isfile(configpath):
            self.no_config(configpath) # if not, create it
            
        self.endpoint_url, self.access_key, self.secret_key, self.bucket_default = self.get_config(configpath) # get config from the file
        
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

        # try to connect to S3
        try:
            s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)
        except:
            print("Something went wrong while trying to connect. Please check your credentials and try again.")
            exit()

        print("Config file created. Please run the script again.")
        exit()


    def parse_options(self):
        '''
        Parse command line options. 
        '''
        # add description if help is called
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                            description='BucketIt is a simple tool for uploading files to S3. \nSee README for more details.',
                                            epilog='Github: https://github.com/sazonovanton/BucketIt') 
        parser.add_argument("file", help="Path to the file you want to upload", type=str)
        parser.add_argument('--filename', default=None, help='Filename to use in the bucket. If not specified, the original filename will be used') 
        parser.add_argument('--date', action='store_true', help='Add date in a format of YYYY/MM/DD before the filename in bucket')
        parser.add_argument('--folder', default=None, help='Folder to upload the file to. If not specified, the file will be uploaded to the root of the bucket')
        parser.add_argument('-r', '--recursive', action='store_true', help='Upload all files in the directory recursively')
        parser.add_argument('-b', '--bucket', default=self.bucket_default, help='Bucket name to upload the file to. If not specified, the default bucket will be used')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')    
        parser.add_argument('--version', action='version', version='%(prog)s 0.5', help='Tool version')
        parser.add_argument('--nofolder', action='store_true', help='Do not create a folder with the same name as the folder with files if recursive is set')
        args = parser.parse_args()

        return args


    def upload(self, args, filepath):
        '''
        Main function. Uploads the file to the bucket. 
        '''
        # get the arguments
        bucket = args.bucket
        verbose = args.verbose
        date = args.date
        filename = args.filename
        folder = args.folder

        filename = filepath.split('/')[-1] if filename is None else filename # if filename is not specified, use the original filename
        now = datetime.now().strftime('%Y/%m/%d/') if date else '' # if date is set, add date in a format of YYYY/MM/DD before the filename
        folder = '' if folder is None else folder + '/' # if folder is not specified, upload to the root of the bucket
        folder_name = args.file.split('/')[-1] + '/' if args.recursive and not args.nofolder else '' # if recursive is set, create a folder with the same name as the folder with files
        
        s3path = folder + now + folder_name + filename # full path to the file in the bucket

        self.s3.upload_file(filepath, bucket, s3path) 
        
        if verbose:
            print("File {} uploaded to bucket '{}' as {}".format(filepath, bucket, s3path)) # print the result if verbose is set

        return True


    def main(self, args):
        '''
        Main function. Uploads the file to the bucket. 
        '''
        if args.bucket is None:
            print("Please specify the bucket name or set the default bucket in the config file")
            return False

        # if recursive is set, upload all files in the directory, otherwise upload the file
        if args.recursive:
            if args.filename is not None:
                print("You cannot specify filename when using --recursive")
                exit()
            for filename in os.listdir(args.file):
                self.upload(args, args.file + '/' + filename)
        else:
            self.upload(args, args.file)

        return True

def cli():
    try:
        b = BucketIt() 
        args = b.parse_options() # parse command line options
        b.main(args) # upload the file
    except Exception as e:
        print("Something went wrong: {}".format(e)) # print error message if something went wrong

if __name__ == "__main__":
    cli()