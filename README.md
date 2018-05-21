# United Way Achievement Club Member Portal

## Description

The United Way Achievement Club aims to empower families to achieve their own goals by helping them set milestones and providing encouragement and rewards along the way. This web application will be used to help the achievement club members and coordinators keep track of progress and reduce dependence on paper forms. 

## How to run

First ensure that you have Python version 2.6+ installed on your machine. To confirm,
open a terminal and run the following command to ensure that python is installed and it is the correct version.

    python --version
    
Contact Sruti at sruti@gatech.edu for AWS credentials and aws cli configuration instructions. Without the AWS credentials on your machine, you will not be able to access the files and images when running the application locally.

Then, follow these steps.


#### 1. Clone this repository


        git clone https://github.com/SrutiG/uw_database.git
#### 2. Navigate to the uw_database folder

        cd uw_database
#### 3. Install the necessary requirements
    
        pip install --user -r requirements.txt
#### 4. Make sure that the run.py file has executable permissions

        chmod +x run.py
#### 5. Run this command

        ./run.py
#### 6. Navigate to the URL *127.0.0.1:8090* in your browser
   A login page should appear. Currently, the test user has the credentials username:*user* and password:*password* and navigates to the coordinator home page.

## How to contribute
Make sure that the ZenHub browser extension is installed to view the task board. It can be installed [here](https://www.zenhub.com/extension) for Chrome or Firefox.


This application is being developed using Flask, a Python framework. All of the server code is located in **app/views.py**. Helper functions are in **app/utils.py**. All of the database models and tables are located in **app/models.py** and the queries are located in **app/db_accessor.py**. Methods related to S3 bucket access/modification are in **app/s3_accessor.py**. The templates are located in **app/templates** and organized by user type. The static files (css, javascript, and images) are located in **app/static**.


The master branch should always be stable. Features that are in progress and need to be completed can be found in the 'Board' section of the repository. When pushing a new feature to GitHub, create a new branch named after that feature, then push the branch to GitHub. Then, make a pull request to the 'dev' branch, and add a description of the feature and the changes that were made.

[Join the Slack Channel](https://join.slack.com/t/achievement-club-db/shared_invite/enQtMzY3Nzk2NzExNjY5LWMxNDE0YTQwZDM5MWYwMDRkYTJmODViNTc2ODljMWZjMGE3YWE3ZDM5MmJmNTMzMmFhNWE4YjdkMTdhNWEzMjM) to ask questions

### Progress

#### General
* Login Page- *complete*
* Navigation- *complete*

#### Member
* Home- *in progress*
* Goals- *in progress*
* Calendar- *not started*
* Messages- *not started*

#### Coordinator
* Home- *in progress*
* Goals- *in progress*
* Approve- *in progress*
* Members- *in progress*
* Clubs- *in progress*

More details about what features have been completed and what there is yet to do can be found in the task board.

### Making changes to the database schema
If you make changes to the database schema by modifying **models.py**, you must create a new migration. 

In order to do this, first give executable permissions to the db_migrations.py file

    chmod +x db_migrate.py
Then, run the file
    
    ./db_migrate.py


If the steps above are not successful or the changes to the schema are major, you need to recreate the database. You must first delete the current set of migrations by deleting the directory **app/db_repository** and the database snapshot in **app/app.db**. 

Then, run this command to give executable permissions to the db_create.py file
                
    chmod +x db_create.py
Same for the db_migrate.py file

    chmod +x db_migrate.py
Then, recreate the database
    
    ./db_create.py
And the migrations
    
    ./db_migate.py

To repopulate the database with some default data, add to the default_data.py file and give executable permissions. Then run it.

    chmod +x default_data.py
Then,

    ./default_data.py

### References

* [Flask](http://flask.pocoo.org/docs/0.12/)
* [Jinja](http://jinja.pocoo.org/)
* [SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
