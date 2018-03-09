'''
Title
-----
db_accessor.py

Description
-----------
Retrieve and add items to the database

'''
from app import db, models
from datetime import datetime


'''
See if a user with the username and password
exists in the database
'''
def loginUser(username, password):
    match = models.User.query.get(username)
    if match == None:
        return None
    if password != match.password:
        return None
    return match

'''
Return all of the members in the database
'''
def getMembers():
    return db.session.query(models.User, models.Member).filter_by(type='member').join(models.Member).all()

'''
Get member by username
'''
def getMember(username):
    member = db.session.query(models.User, models.Member).filter_by(username=username).first()
    return member

def editProfilePic(username):
    user = models.User.query.get(username)
    user.profile_picture = username + '.jpg'
    db.session.commit()

'''
Update a member after edit profile
'''
def updateMember(member_data, username):
    member = models.User.query.get(username)
    member.birth_date = datetime.strptime(member_data['birth_date'], '%Y-%m-%d')
    member.address_street = member_data['address_street']
    member.address_state = member_data['address_state']
    member.address_city = member_data['address_city']
    member.address_zip = member_data['address_zip']
    member.email = member_data['email']
    old_phones = models.Member_Phone.query.filter_by(username=username)
    for number in old_phones:
        if number.phone in member_data['phone_numbers']:
            index = member_data['phone_numbers'].index(number.phone)
            del member_data['phone_numbers'][index]
        else:
            models.Member_Phone.query.filter_by(username=username, phone=number.phone).delete()
    for phone in member_data['phone_numbers']:
        db.session.add(models.Member_Phone(username=username, phone=phone))
    db.session.commit()

'''
Get member phone numbers by username
'''
def getPhoneNumbers(username):
    phone_numbers = models.Member_Phone.query.filter_by(username=username).all()
    return phone_numbers

'''
Get coordinator by username
'''
def getCoordinator(username):
    return models.User.query.get(username)

'''
Return all of the coordinators in the database
'''
def getCoordinators():
    return models.Coordinator.query.all()

'''
Add a new member to the database
'''
def addMember(member_obj):
    # general contains general fields like username, password, join date...etc.
    general = member_obj['general']

    # the enrollment form has basic data like first name, last name, email, phone numbers...etc.
    enrollment_form = member_obj['enrollment_form']

    # demographic data has info on the demographics such as race, marital status...etc.
    demographic_data = member_obj['demographic_data']

    # self sufficiency matrix is a dictionary with dates as keys and dictionaries as values containing questions and answers
    self_sufficiency_matrix = member_obj['self_sufficiency_matrix']

    # self efficacy quiz is a dictionary in the same structure as self sufficiency matrix
    self_efficacy_quiz = member_obj['self_efficacy_quiz']

    # TODO: parse values from these dictionaries and create a new member based on them
    # first, db.session.add(models.User(username=username ...))
    # then, db.session.add(models.Member(username=username ...))
    # if applicable, iterate through phone numbers and do db.session.add(models.Member_Phone(username=username, phone=phone))
    # if applicable, same thing for children to Child table
    # if applicable, same thing for the db tables Member_Sources_Of_Income, Member_Assets, Member_Medical_Issues,
    # Member_Wars_Served, Member_Self_Sufficiency_Matrix, Member_Self_Efficacy_Quiz
    # lastly, db.session.commit()

'''
Get the general information for a member to put into the member modal
'''
def getGeneral(username):
    member = models.User.query.get(username)
    general = {}
    general['username'] = username
    general['password'] = member.password
    general['club_name'] = member.member[0].club_name
    general['join_date'] = member.member[0].join_date
    general['commitment_pledge'] = member.member[0].commitment_pledge
    general['photo_release'] = member.member[0].photo_release
    return general

def getEnrollmentForm(username):
    member = models.User.query.get(username)
    enrollment_form = {}
    enrollment_form['first_name'] = member.first_name
    enrollment_form['last_name'] = member.last_name
    enrollment_form['address_street'] = member.address_street
    enrollment_form['address_state'] = member.address_state
    enrollment_form['address_city'] = member.address_city
    enrollment_form['address_zip'] = member.address_zip
    enrollment_form['birth_date'] = member.birth_date
    enrollment_form['email'] = member.email
    enrollment_form['phone_numbers'] = []
    for entry in member.member[0].phone_numbers:
        enrollment_form['phone_numbers'].append(entry.phone)
    enrollment_form['spouse_first_name'] = member.spouse_first_name
    enrollment_form['spouse_last_name'] = member.spouse_last_name
    return enrollment_form