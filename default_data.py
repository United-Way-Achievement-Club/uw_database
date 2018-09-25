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
from passlib.context import CryptContext
import os

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

date = datetime.strptime('2018-03-01', '%Y-%m-%d')
child_birth_date = datetime.strptime('2010-02-11', '%Y-%m-%d')
birth_date = datetime.strptime('1997-01-24', '%Y-%m-%d')
password = pwd_context.encrypt(os.environ['UW_PASSWORD'])

# Coordinators
# coordinator = models.User(username='coordinator', password=password, super_admin=False, email='coordinator@achievementclub.com', profile_picture='coordinator.jpg', first_name='Jane', last_name='Doe', type='coordinator', address_street='123 Example Ave SE', address_city='Atlanta', address_state='GA', address_zip='30318', birth_date=birth_date)
# user = models.User(username='user', profile_picture='user.jpg', super_admin=True, email='user@achievementclub.com', password=password, first_name='Bob', last_name='Smith', type='coordinator', address_street='123 Example Ave SE', address_city='Atlanta', address_state='GA', address_zip='30318', birth_date=birth_date)
amy = models.User(username='abarrow', password=password, super_admin=True, email='abarrow@unitedwayatlanta.org', profile_picture='abarrow.jpg', first_name='Amy', last_name='Barrow', type='coordinator')


# db.session.add(coordinator)
# db.session.add(user)
db.session.add(amy)

# db.session.add(models.User_Phone(username='coordinator', phone='0001212222'))
# db.session.add(models.User_Phone(username='coordinator', phone='2223354444'))
# db.session.add(models.User_Phone(username='user', phone='0001122222'))
# db.session.add(models.User_Phone(username='user', phone='2223834444'))

# Clubs

pebblebrook_high = models.Club(club_name='Pebblebrook High School', address_street='991 Old Alabama Rd SW', address_city='Mableton', address_zip='30126', address_state='GA', address_county='Cobb', longitude=-84.5818547, latitude=33.8068817, create_time=date, created_by='abarrow')
united_way = models.Club(club_name='United Way of Greater Atlanta', address_street='40 Courtland St NE #300', address_city='Atlanta', address_zip='30303', address_state='GA', address_county='Fulton', longitude=-84.3845972, latitude=33.7552402, create_time=date, created_by='abarrow')
db.session.add(pebblebrook_high)
db.session.add(united_way)


# coordinator.clubs.append(pebblebrook_high)
# coordinator.clubs.append(united_way)
# user.clubs.append(pebblebrook_high)
amy.clubs.append(united_way)

# db.session.add(coordinator)
# db.session.add(user)
db.session.add(amy)

# Members

# db.session.add(models.User(username='srutig', password=password, first_name='Sruti', last_name='Guhathakurta', email='sruti.guhathakurta@gmail.com', profile_picture='srutig.jpg', type='member', gender='Female', race='asian-indian', address_street='123 Example Ave SE', address_city='Atlanta', address_state='GA', address_zip='30318', birth_date=birth_date))
# db.session.add(models.Member(username='srutig', join_date=date, club_name='Pebblebrook High School', commitment_pledge=date, photo_release=date, education='some-college', marital_status='single', income='10000', has_car='true', employment_status='employed-part-time'))
# db.session.add(models.User_Phone(username='srutig', phone='1234567890'))
# db.session.add(models.User_Phone(username='srutig', phone='0987654321'))
# db.session.add(models.Child(parent='srutig', child_first_name='Fake', child_last_name='Child', child_birth_date=child_birth_date))
# db.session.add(models.Member_Sources_Of_Income(username='srutig', income_source='other'))
# db.session.add(models.Member_Sources_Of_Income(username='srutig', income_source='work'))
# db.session.add(models.Member_Assets(username='srutig', asset='savings-account'))
# db.session.add(models.Member_Assets(username='srutig', asset='stocks'))
# db.session.add(models.Member_Self_Sufficiency_Matrix(username='srutig', assessment_date=date, housing="4", employment="5", income="5", food="5", child_care="1", childrens_education="1", adult_education="4", health_care_coverage="5", life_skills="5", family_social_relations="5", mobility="5", community_involvement="5", parenting_skills="1", legal="5", mental_health="5", substance_abuse="5", safety="5", disabilities="5", other="5"))


# db.session.add(models.User(username='hpotter', password=password, first_name='Harry', last_name='Potter', email='harry.potter@gmail.com', profile_picture='hpotter.jpg', type='member', gender='Male', race='white', address_street='123 Hogwarts Rd', address_city='Atlanta', address_state='GA', address_zip='30313', birth_date=birth_date))
# db.session.add(models.Member(username='hpotter', join_date=date, club_name='Pebblebrook High School', commitment_pledge=date, photo_release=date, education='some-college', marital_status='single', income='200000'))
# db.session.add(models.User_Phone(username='hpotter', phone='0001112222'))
# db.session.add(models.User_Phone(username='hpotter', phone='2223334444'))
#
# db.session.add(models.User(username='ajolie', password=password, first_name='Angelina', last_name='Jolie', email='angelina.jolie@gmail.com', profile_picture='ajolie.jpg', type='member', gender='Female', race='white', address_street='123 Jolie Rd', address_city='Los Angeles', address_state='CA', address_zip='90210', birth_date=birth_date))
# db.session.add(models.Member(username='ajolie', join_date=date, club_name='United Way of Greater Atlanta', commitment_pledge=date, photo_release=date, education='some-college', marital_status='married', income='200000'))
# db.session.add(models.User_Phone(username='ajolie', phone='0002112222'))
# db.session.add(models.User_Phone(username='ajolie', phone='2223934444'))


# Categories

db.session.add(models.Categories(category_name="Education"))
db.session.add(models.Categories(category_name="Health"))
db.session.add(models.Categories(category_name="Income"))
db.session.add(models.Categories(category_name="Community"))
db.session.add(models.Categories(category_name="Civic"))

# Goals

db.session.add(models.Goals(goal_name="Focus On My Child's Future", goal_category="Education", num_of_steps=3))

db.session.add(models.Steps(step_name="Be Active At Home", goal_name="Focus On My Child's Future", step_num=1, num_of_proofs=3))
db.session.add(models.Steps(step_name="Be Active At The School", goal_name="Focus On My Child's Future", step_num=2, num_of_proofs=3))
db.session.add(models.Steps(step_name="Plan For The Future", goal_name="Focus On My Child's Future", step_num=3, num_of_proofs=2))

db.session.add(models.Proof(proof_name="Copy of a reading log", step_name="Be Active At Home", description="Read to my child every night or have my child read to me every night for one month", proof_num=1))
db.session.add(models.Proof(proof_name="Copy or a photo of the library cards", step_name="Be Active At Home", description="Get a library card for me and my child", proof_num=2))
db.session.add(models.Proof(proof_name="Copy or a photo of the homework", step_name="Be Active At Home", description="Help my child with homework every night for a month", proof_num=3))

db.session.add(models.Proof(proof_name="Letter from the teacher on school letterhead", step_name="Be Active At The School", description="Attend a parent-teacher conference", proof_num=1))
db.session.add(models.Proof(proof_name="Letter from the volunteer leader", step_name="Be Active At The School", description="Volunteer at my child's school", proof_num=2))
db.session.add(models.Proof(proof_name="Letter from the committee leader", step_name="Be Active At The School", description="Join a committee at my child's school", proof_num=3))

db.session.add(models.Proof(proof_name="Copy of your plan", step_name="Plan For The Future", description="Discover education requirements for my child's dream job. Make a plan for how they can meet these requirements", proof_num=1))
db.session.add(models.Proof(proof_name="Letter from the interviewee", step_name="Plan For The Future", description="Together, interview someone who works at your child's dream job", proof_num=2))

# particular user's goal data

# goal = models.Goals.query.get("Focus On My Child's Future")
# db.session.add(models.Member_Goals(username='hpotter', goal_name="Focus On My Child's Future", significance='', goal_status='in_progress', date_completed=None))
# db.session.add(models.Member_Goals(username='srutig', goal_name="Focus On My Child's Future", significance='', goal_status='in_progress', date_completed=None))
#
# for step in goal.steps:
#     db.session.add(models.Member_Steps(username='hpotter', step_name=step.step_name, goal_name=goal.goal_name, step_status='in_progress',proofs_completed=0))
#     db.session.add(models.Member_Steps(username='srutig', step_name=step.step_name, goal_name=goal.goal_name, step_status='in_progress',proofs_completed=0))
#     for proof in step.proofs:
#         db.session.add(models.Member_Proofs(username='hpotter', proof_name=proof.proof_name, step_name=step.step_name))
#         db.session.add(models.Member_Proofs(username='srutig', proof_name=proof.proof_name, step_name=step.step_name))


db.session.commit()
