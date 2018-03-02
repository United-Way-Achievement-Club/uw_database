#!/usr/bin/env python2.7
'''
Title
-----
default_data.py

Description
-----------
Add data to the database after schema is changed

'''

from app import db, models
from datetime import datetime

date = datetime.strptime('2018-03-01', '%Y-%m-%d')
birth_date = datetime.strptime('1997-01-24', '%Y-%m-%d')

db.session.add(models.Club(club_name='Pebblebrook High School'))

db.session.add(models.User(username='srutig', password='password', first_name='Sruti', last_name='Guhathakurta', email='sruti.guhathakurta@gmail.com', profile_picture='sruti.png', type='member', gender='Female', race='asian-indian', address_street='351 Sinclair Ave NE', address_city='Atlanta', address_state='GA', address_zip='30307', birth_date=birth_date))
db.session.add(models.Member(username='srutig', join_date=date, club_name='Pebblebrook High School', commitment_pledge=date, photo_release=date, education='some-college', marital_status='single', income='10000'))
db.session.add(models.Member_Phone(username='srutig', phone='1234567890'))
db.session.add(models.Member_Phone(username='srutig', phone='0987654321'))

db.session.add(models.User(username='coordinator', password='password', first_name='Example', last_name='Coordinator', type='coordinator'))

db.session.commit()
