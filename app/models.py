'''
Title
-----
models.py

Description
-----------
Database schema

'''
from app import db

# ============================================== USER ==============================================

'''
Coordinator-Club table (n-n)
'''
Coordinator_Club = db.Table('Coordinator_Clubs',
    db.Column('username', db.String(64), db.ForeignKey('user.username'), primary_key=True),
    db.Column('club_name', db.String(120), db.ForeignKey('club.club_name'), primary_key=True)
)

'''
General user table, can be either member or coordinator
'''
class User(db.Model):
    username = db.Column(db.String(64), index=True, primary_key=True)
    type = db.Column(db.String(64))
    password = db.Column(db.String(120))
    profile_picture = db.Column(db.String(150))
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    gender = db.Column(db.String(64))
    race = db.Column(db.String(64))
    address_street = db.Column(db.String(150))
    address_city = db.Column(db.String(64))
    address_state = db.Column(db.String(64))
    county = db.Column(db.String(64))
    address_zip = db.Column(db.String(20))
    birth_date = db.Column(db.DateTime)
    tags = db.relationship('Club', secondary=Coordinator_Club, lazy='subquery',
           backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % (self.username)

'''
Member table for info specific to a member
'''
class Member(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('user.username'), primary_key=True)
    join_date = db.Column(db.DateTime)
    club_name = db.Column(db.String(120), db.ForeignKey('club.club_name'))
    commitment_pledge = db.Column(db.DateTime)
    photo_release = db.Column(db.DateTime)
    education = db.Column(db.String(120))
    marital_status = db.Column(db.String(120))
    income = db.Column(db.String(120))
    credit_score = db.Column(db.Integer)
    employment_status = db.Column(db.String(120))
    referral_source = db.Column(db.String(120))
    spouse_first_name = db.Column(db.String(120))
    spouse_last_name = db.Column(db.String(120))
    english_proficiency = db.Column(db.String(120))
    english_reading_level = db.Column(db.String(120))
    english_writing_level = db.Column(db.String(120))
    has_car = db.Column(db.Boolean)
    has_health_insurance = db.Column(db.Boolean)
    has_primary_care_doctor = db.Column(db.Boolean)
    enrolled_in_military = db.Column(db.Boolean)
    has_served_in_military = db.Column(db.Boolean)
    income_sources = db.relationship('Member_Sources_Of_Income', backref='member', lazy=True)
    assets = db.relationship('Member_Assets', backref='member', lazy=True)
    phone_numbers = db.relationship('Member_Phone', backref='member', lazy=True)
    medical_issues = db.relationship('Member_Medical_Issues', backref='member', lazy=True)
    wars_served = db.relationship('Member_Wars_Served', backref='member', lazy=True)
    self_sufficiency_matrices = db.relationship('Member_Self_Sufficiency_Matrix', backref='member', lazy=True)
    self_efficacy_quizzes = db.relationship('Member_Self_Efficacy_Quiz', backref='member', lazy=True)

'''
Member-Sources of Income (1-n)
'''
class Member_Sources_Of_Income(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    income_source = db.Column(db.String(64), primary_key=True)

'''
Member-Assets (1-n)
'''
class Member_Assets(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    asset = db.Column(db.String(64), primary_key=True)

'''
Member-Phone Numbers (1-n)
'''
class Member_Phone(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    phone = db.Column(db.String(32), primary_key=True)

'''
Member-Medical Issues (1-n)
'''
class Member_Medical_Issues(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    medical_issue = db.Column(db.Text, primary_key=True)

'''
Member-Wars Served (1-n)
'''
class Member_Wars_Served(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    war_served = db.Column(db.String(120), primary_key=True)

'''
Member-Self Sufficiency Matrix results (1-n)
'''
class Member_Self_Sufficiency_Matrix(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    assesment_date = db.Column(db.DateTime, primary_key=True)
    housing = db.Column(db.Integer)
    employment = db.Column(db.Integer)
    income = db.Column(db.Integer)
    food = db.Column(db.Integer)
    child_care = db.Column(db.Integer)
    childrens_education = db.Column(db.Integer)
    adult_education = db.Column(db.Integer)
    health_care_coverage = db.Column(db.Integer)
    life_skills = db.Column(db.Integer)
    family_social_relations = db.Column(db.Integer)
    mobility = db.Column(db.Integer)
    community_involvement = db.Column(db.Integer)
    parenting_skills = db.Column(db.Integer)
    legal = db.Column(db.Integer)
    mental_health = db.Column(db.Integer)
    substance_abuse = db.Column(db.Integer)
    safety = db.Column(db.Integer)
    disabilities = db.Column(db.Integer)
    other = db.Column(db.Integer)

'''
Member-Self Efficacy Quiz Results (1-n)
'''
class Member_Self_Efficacy_Quiz(db.Model):
    username = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    assesment_date = db.Column(db.DateTime, primary_key=True)
    question_1 = db.Column(db.Integer)
    question_2 = db.Column(db.Integer)
    question_3 = db.Column(db.Integer)
    question_4 = db.Column(db.Integer)
    question_5 = db.Column(db.Integer)
    question_6 = db.Column(db.Integer)
    question_7 = db.Column(db.Integer)
    question_8 = db.Column(db.Integer)
    question_9 = db.Column(db.Integer)
    question_10 = db.Column(db.Integer)
    question_11 = db.Column(db.Integer)
    question_12 = db.Column(db.Integer)

'''
Member-Child (1-n)
'''
class Child(db.Model):
    parent = db.Column(db.String(64), db.ForeignKey('member.username'), primary_key=True)
    first_name = db.Column(db.String(64), primary_key=True)
    last_name = db.Column(db.String(64), primary_key=True)
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.String(64))
    grade_level = db.Column(db.Integer)
    grades = db.Column(db.String(64))
    school = db.Column(db.String(120))

# ============================================== GOALS ==============================================


# ============================================== OTHER ==============================================

'''
Achievement Club locations
'''
class Club(db.Model):
    club_name = db.Column(db.String(120), primary_key=True)
    address_street = db.Column(db.String(200))
    address_state = db.Column(db.String(64))
    address_zip = db.Column(db.String(20))
    address_county = db.Column(db.String(64))