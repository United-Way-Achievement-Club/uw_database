# United Way Achievement Club Member Portal

## Description

The United Way Achievement Club aims to empower families to achieve their own goals by helping them set milestones and providing encouragement and rewards along the way. This web application will be used to help the achievement club members and coordinators keep track of progress and reduce dependence on paper forms. 

## How to run

First ensure that you have Python version 2.6+ installed on your machine. To confirm,
run the following command to ensure that python is installed and it is the correct version.

    python --version
    

Then, open a terminal and follow these steps.


#### 1. Clone this repository


        git clone https://github.com/SrutiG/uw_database.git
#### 2. Navigate to the uw_database folder

        cd uw_database
#### 3. Install the necessary requirements
    
        pip install -r requirements.txt
#### 4. Run this command

        python run.py
#### 5. Navigate to the URL *127.0.0.1:8090* in your browser
   A login page should appear. Currently, the test user has the credentials username:*user* and password:*pass* and navigates to the coordinator home page.

## How to contribute
Make sure that the ZenHub browser extension is installed to view the task board. It can be installed [here](https://www.zenhub.com/extension) for Chrome or Firefox.


This application is being made using Flask, a Python framework. All of the server code is located in the **app/views.py** folder. All of the database models and tables are located in **app/models.py**. The templates are located in **app/templates** and organized by user type. The static files (css, javascript, and images) are located in **app/static**.


The master branch should always be stable. Features that are in progress and need to be completed can be found in the 'Board' section of the repository. When pushing a new feature to GitHub, create a new branch named after that feature, then push the branch to GitHub. Then, make a pull request to the 'dev' branch, and add a description of the feature and the changes that were made.

### References

* [Flask](http://flask.pocoo.org/docs/0.12/)
* [Jinja](http://jinja.pocoo.org/)
* [SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)