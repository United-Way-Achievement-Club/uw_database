'''
Get files in the s3 bucket
'''

import boto3
import requests
import boto3.session

s3session = boto3.session.Session(region_name='us-east-2')

s3 = boto3.resource('s3')
s3Client = boto3.client('s3', config= boto3.session.Config(signature_version='s3v4', s3={'addressing_style':'path'}))
bucket_name = 'achievement-club-private'

'''
Get a presigned url for the users profile picture
'''
def getProfilePicture(username):
    try:
        picture_url = s3Client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': 'profile_pictures/' + username + '.jpg'})
    except Exception as e:
        print e.message
        picture_url = None
    return picture_url

'''
Upload a user's profile picture to the bucket
'''
def uploadProfilePicture(username, file):
    try:
        s3.Bucket(bucket_name).put_object(Key='profile_pictures/' + username + '.jpg', Body=file)
        print 'successfully uploaded image for ' + username
    except Exception as e:
        print e.message


