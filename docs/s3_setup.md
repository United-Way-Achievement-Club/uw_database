# Set up an S3 Bucket

## Purpose

These are instructions for setting up an S3 Bucket for this application. This bucket will contain the directories and be configured for this application only. This is not a general tutorial for setting up an S3 Bucket.

## Description

The United Way Achievement Club S3 Bucket will contain profile pictures, club photos, and goal documents.

## Prerequisites

- An Amazon Web Services Account

## Steps

#### First, create an S3 Bucket

1. Login to your Amazon Web Services Account.

1. Click **Services** in the AWS Menu and then **S3** under Storage.

1. Click the **Create Bucket** button at the top

1. Enter a name for your new bucket. Click **Next**

1. Ignore this page (Versioning, Server access logging... etc.). Just click **Next**.

1. Ensure that the owner has all permissions. 

    **Manage public permissions** should remain as **Do not grant public read access to this bucket**.
     
    **Manage System Permissions** should remain as **Do not grant Amazon S3 Log delivery group write access to this bucket**.
    
    Then, click **Next**

1. Review everything and click **Create Bucket**

1. Click on your newly created bucket

1. Click **Create folder**. Name the folder **profile_pictures**.

1. Repeat the last step to create folders **club_pictures** and **goal_docs**.

1. (Optional) Populate the profile pictures folder with the images in this repository under **app/static/images/profile_pictures**. 

    In order to do this, clone this GitHub repo (steps to clone the repo are in the main README file). Then, go back to your S3 bucket console, and click on the **profile_pictures** folder. Select **Upload** and upload all profile pictures from that directory to your bucket.
    
    This step will ensure that the default user profile pictures will show up without having to upload new ones.
    
1. Navigate to the **Permissions** tab in your new S3 bucket. Click **Bucket Policy**. Next to the **Bucket policy editor** header, there will be an ARN. Keep note of this because you will need it later.

1. Look at the URL of the page you are on currently. It will look something like

    https://s3.console.aws.amazon.com/s3/buckets/*your-bucket-name*/?region=*your bucket region*&tab=permissions
    
    Take note of the region. It will be something like *us-west-1*, or *us-east-2*.

#### Then, create an IAM user

1. Click **Services** in the AWS Menu and then **IAM** under Security, Identity, & Compliance.

1. Click on **Users** in the side navigation bar

1. Select **Add User** at the top of the page

1. Enter any username. Select **Programmatic Access** for Access Type

1. The next page will ask to set permissions for this user. Click on **Attach existing policies directly**.

1. You want this user to only have access to the s3 bucket you created earlier. Click **Create Policy**.

1. In the visual editor, select **Choose a service** and select **S3**

1. For actions, select **All S3 Actions**. 

    *Optional: For extra security, you can select only **GetObject** under Read, and **DeleteObject** and **PutObject** under Write*

1. For Resources, ensure that **Specific** is selected. In the bucket section, click **Add ARN**.

1. Enter the ARN for the bucket you created in the previous section which you took note of. Then, click **Add**.

1. It will ask you to review the policy. Give it a name and description of your choosing. Remember the name for the next step. Then click **Create Policy**.

1. This should bring you back to the previous window with the list of policies. Search for the policy name from the previous step and check the checkbox for it. Then, click **Next: Review** at the bottom of the page.

1. Review the details and click **Create User**.

1. The next page will show you an Access Key ID and Secret Access Key. Ensure that these do not get into the wrong hands. You should download the csv (click **Download .csv** at the top) file and store it in a secure location. You will need these later.

1. Set these three environment variables on your machine.

    **AWS_ACCESS_KEY_ID**: your access key id
    
    **AWS_SECRET_ACCESS_KEY**: your secret access key
    
    **AWS_DEFAULT_REGION**: the region of your S3 bucket which you took note of before
    
#### Now, you should be able to access the file system when running the application.

[Back to Home](../README.md)



