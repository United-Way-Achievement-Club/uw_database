'''
Title
-----
db_config.py

Description
-----------
Current state of the database tables

'''

from app import db, models, utils
import csv
from shutil import make_archive
from datetime import datetime
from s3_accessor import uploadDBBackup, getLatestDBBackup
import os

backups_path = os.path.join(os.getcwd(), "app/db_backups/")
tables = [
    'User',
    'Member',
    'Member_Sources_Of_Income',
    'Member_Assets',
    'User_Phone',
    'Member_Medical_Issues',
    'Member_Wars_Served',
    'Member_Self_Sufficiency_Matrix',
    'Member_Self_Efficacy_Quiz',
    'Child',
    'Member_Goals',
    'Member_Steps',
    'Member_Proofs',
    'Goals',
    'Steps',
    'Proof',
    'Categories',
    'Club',
    'Club_Photos',
]

def getTables():
    table_dict = {}
    for table in tables:
        table_dict[table] = len(getattr(models, table).query.all())
    return table_dict

def write_table_to_csv(table_name):
    values = getattr(models, table_name).query.all()
    with open(backups_path + table_name + '.csv', 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        keys = [utils.remove_non_ascii(column.key) for column in getattr(models, table_name).__table__.columns]
        csvwriter.writerow(keys)

        for value in values:
            try:
                csvwriter.writerow([utils.remove_non_ascii(getattr(value, key)) for key in keys])
            except UnicodeEncodeError as e:
                print e.message

def createDBBackups():
    # write all tables to csv file
    for table in tables:
        write_table_to_csv(table)

    # write coordinator clubs
    users = models.User.query.filter_by(type="coordinator").all()
    with open(backups_path + 'Coordinator_Club.csv', 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for user in users:
            csvwriter.writerow([user.username] + [utils.remove_non_ascii(club.club_name) for club in user.clubs])

    make_archive('app/db_backups', 'zip', backups_path)
    file = open('app/db_backups.zip', 'rb')
    file_name = 'db_backups_' + datetime.now().strftime("%Y-%m-%d") + '.zip'
    uploadDBBackup(file_name, file)

def createDBBackupsAndGetURL():
    createDBBackups()
    url = getLatestDBBackup()
    os.remove('app/db_backups.zip')
    return url
