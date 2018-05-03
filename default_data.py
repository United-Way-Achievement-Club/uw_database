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
child_birth_date = datetime.strptime('2010-02-11', '%Y-%m-%d')
birth_date = datetime.strptime('1997-01-24', '%Y-%m-%d')

db.session.add(models.Club(club_name='Pebblebrook High School'))

db.session.add(models.User(username='srutig', password='password', first_name='Sruti', last_name='Guhathakurta', email='sruti.guhathakurta@gmail.com', profile_picture='srutig.jpg', type='member', gender='Female', race='asian-indian', address_street='123 Example Ave SE', address_city='Atlanta', address_state='GA', address_zip='30318', birth_date=birth_date))
db.session.add(models.Member(username='srutig', join_date=date, club_name='Pebblebrook High School', commitment_pledge=date, photo_release=date, education='some-college', marital_status='single', income='10000', has_car='true', employment_status='employed-part-time'))
db.session.add(models.User_Phone(username='srutig', phone='1234567890'))
db.session.add(models.User_Phone(username='srutig', phone='0987654321'))
db.session.add(models.Child(parent='srutig', child_first_name='Fake', child_last_name='Child', child_birth_date=child_birth_date))
db.session.add(models.Member_Sources_Of_Income(username='srutig', income_source='other'))
db.session.add(models.Member_Sources_Of_Income(username='srutig', income_source='work'))
db.session.add(models.Member_Assets(username='srutig', asset='savings-account'))
db.session.add(models.Member_Assets(username='srutig', asset='stocks'))
db.session.add(models.Member_Self_Sufficiency_Matrix(username='srutig', assessment_date=date, housing="4", employment="5", income="5", food="5", child_care="1", childrens_education="1", adult_education="4", health_care_coverage="5", life_skills="5", family_social_relations="5", mobility="5", community_involvement="5", parenting_skills="1", legal="5", mental_health="5", substance_abuse="5", safety="5", disabilities="5", other="5"))


db.session.add(models.User(username='hpotter', password='password', first_name='Harry', last_name='Potter', email='harry.potter@gmail.com', profile_picture='hpotter.jpg', type='member', gender='Male', race='white', address_street='123 Hogwarts Rd', address_city='Atlanta', address_state='GA', address_zip='30313', birth_date=birth_date))
db.session.add(models.Member(username='hpotter', join_date=date, club_name='United Way', commitment_pledge=date, photo_release=date, education='some-college', marital_status='single', income='200000'))
db.session.add(models.User_Phone(username='hpotter', phone='0001112222'))
db.session.add(models.User_Phone(username='hpotter', phone='2223334444'))

db.session.add(models.User(username='coordinator', password='password', email='coordinator@achievementclub.com', profile_picture='coordinator.jpg', first_name='Example', last_name='Coordinator', type='coordinator', address_street='123 Example Ave SE', address_city='Atlanta', address_state='GA', address_zip='30318', birth_date=birth_date))
db.session.add(models.User(username='user', profile_picture='user.jpg', email='user@achievementclub.com', password='password', first_name='Another', last_name='Coordinator', type='coordinator', address_street='123 Example Ave SE', address_city='Atlanta', address_state='GA', address_zip='30318', birth_date=birth_date))

db.session.add(models.User_Phone(username='coordinator', phone='0001212222'))
db.session.add(models.User_Phone(username='coordinator', phone='2223354444'))
db.session.add(models.User_Phone(username='user', phone='0001122222'))
db.session.add(models.User_Phone(username='user', phone='2223834444'))

db.session.commit()
