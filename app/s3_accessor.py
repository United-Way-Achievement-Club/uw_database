'''

Title
------
s3_accessor.py

Description
------------
Access and modify files in the s3 bucket

'''

import boto3
import boto3.session

bucket_name = 'achievement-club-private'
region_name = 'us-east-2'

s3session = boto3.session.Session(region_name=region_name)

s3 = boto3.resource('s3')
s3Client = boto3.client('s3', config= boto3.session.Config(signature_version='s3v4', s3={'addressing_style':'path'}))


'''
Get a presigned url for the users profile picture
'''
def getProfilePicture(profile_picture):
    try:
        picture_url = s3Client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': 'profile_pictures/' + profile_picture})
    except Exception as e:
        print e.message
        picture_url = 'static/images/profile_pictures/default_profile_pic.png'
    return picture_url

'''
Upload a user's profile picture to the bucket
'''
def uploadProfilePicture(profile_picture, file):
    try:
        s3.Bucket(bucket_name).put_object(Key='profile_pictures/' + profile_picture, Body=file)
        print 'successfully uploaded image ' + profile_picture
    except Exception as e:
        print e.message

'''
Upload a club photo to the bucket
'''
def uploadClubPicture(file_name, file):
    try:
        # this will be the file_name: club_name + '_' + datetime.now().strftime("%Y%m%d%H%M%S")
        club_name = file_name.split('_')[0]
        s3.Bucket(bucket_name).put_object(Key='club_pictures/' + file_name, Body=file)
        print 'successfully uploaded image for ' + club_name
    except Exception as e:
        print e.message

'''
get all pictures for a club
'''
def getClubPictures(club_name, club_pictures):
    urls = []
    for picture in club_pictures:
        try:
            print 'getting picture for ' + club_name
            picture_url = s3Client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': 'club_pictures/' + picture})
            urls.append(picture_url)
        except Exception as e:
            print e.message
    return urls

'''
Upload a goal document for a proof
'''
def uploadGoalDocument(file_name, file):
    try:
        # this will be the file_name: username + '_' + proof_name + '_' + datetime.now().strftime("%Y%m%d%H%M%S")
        comps = file_name.split('_')
        username = comps[0]
        proof_name = comps[1]
        s3.Bucket(bucket_name).put_object(Key='goal_docs/' + file_name, Body=file)
        print 'successfully uploaded proof ' + proof_name + ' for ' + username
        return True
    except Exception as e:
        print e.message
        return False

'''
Delete a goal document for a proof
'''
def removeGoalDocument(file_name):
    try:
        s3.Object(bucket_name, 'goal_docs/' + file_name).delete()
        print 'successfully deleted proof ' + file_name
        return True
    except Exception as e:
        print e.message
        return False



