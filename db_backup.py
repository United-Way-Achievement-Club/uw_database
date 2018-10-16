#!/usr/bin/env python2.7
'''
Title
-----
db_backup.py

Description
-----------
Back up the database to csv files

'''

from app import db, models
import csv

backups_path = "app/db_backups/"
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

def write_table_to_csv(table_name):
    values = getattr(models, table_name).query.all()
    with open(backups_path + table_name + '.csv', 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        keys = [column.key for column in getattr(models, table_name).__table__.columns]
        csvwriter.writerow(keys)

        for value in values:
            csvwriter.writerow([getattr(value, key) for key in keys])

# write all tables to csv file
for table in tables:
    write_table_to_csv(table)

# write coordinator clubs
users = models.User.query.filter_by(type="coordinator").all()
with open(backups_path + 'Coordinator_Club.csv', 'w') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter=',',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for user in users:
        csvwriter.writerow([user.username] + [club.club_name for club in user.clubs])




