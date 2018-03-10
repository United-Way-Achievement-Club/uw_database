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
Compare the updated member to the old member and
update necessary fields in the database
'''
def editMember(updated_member, old_member):
    # TODO: implement edit member function
    # compare each field in the updated member and old member
    # only make database queries when there is a difference
    # in one of the fields.

    # NOTE: the username will be the same in updated_member and old_member
    # because they shouldn't be able to change their username.
    user = models.User.query.get(old_member['general']['username'])

    # in order to access fields in the 'User' table, just access the field directly (ex. user.password)
    # in order to access fields in the 'Member' table, say user.member[0].<field_name> (ex. user.member[0].join_date)

    general = updated_member['general']
    old_general = old_member['general']
    for key in general:
        if general[key] != old_general[key]:
            print "updating item in database"
            print key
            print general[key]
            # make a database query here to update the value

    # do the same for enrollment form, demographic data, self sufficiency matrix, self efficacy quiz
    # at the end, db.session.commit()


'''
Get the general information for a member to put into the member modal
'''
def getGeneral(username):
    member = models.User.query.get(username)
    general = {}
    general['username'] = username
    general['password'] = member.password
    general['club_name'] = member.member[0].club_name
    general['join_date'] = datetime.strftime(member.member[0].join_date, '%Y-%m-%d')
    general['commitment_pledge'] = datetime.strftime(member.member[0].commitment_pledge, '%Y-%m-%d')
    general['photo_release'] = datetime.strftime(member.member[0].photo_release, '%Y-%m-%d')
    general['profile_picture'] = member.profile_picture
    return general

'''
Get the enrollment form information for a member to put into the member modal
'''
def getEnrollmentForm(username):
    member = models.User.query.get(username)
    children = models.Child.query.filter_by(parent=username)
    enrollment_form = {}
    enrollment_form['first_name'] = member.first_name
    enrollment_form['last_name'] = member.last_name
    enrollment_form['address_street'] = member.address_street
    enrollment_form['address_state'] = member.address_state
    enrollment_form['address_city'] = member.address_city
    enrollment_form['address_zip'] = member.address_zip
    enrollment_form['birth_date'] = datetime.strftime(member.birth_date, '%Y-%m-%d')
    enrollment_form['email'] = member.email
    enrollment_form['phone_numbers'] = []
    for entry in member.member[0].phone_numbers:
        enrollment_form['phone_numbers'].append(entry.phone)
    enrollment_form['spouse_first_name'] = member.member[0].spouse_first_name
    enrollment_form['spouse_last_name'] = member.member[0].spouse_last_name
    enrollment_form['children'] = []
    for entry in children:
        child_obj = {}
        child_obj['child_first_name'] = entry.first_name
        child_obj['child_last_name'] = entry.last_name
        child_obj['child_gender'] = entry.gender
        child_obj['child_birth_date'] = datetime.strftime(entry.birth_date, '%Y-%m-%d')
        child_obj['child_school'] = entry.school
        child_obj['child_grade_level'] = entry.grade_level
        child_obj['child_grades'] = entry.grades
        enrollment_form['children'].append(child_obj)
    return enrollment_form

'''
Get the demographic data information for a member to put into the member modal
'''
def getDemographicData(username):
    member = models.User.query.get(username)
    demographic_data = {}
    demographic_data['gender'] = member.gender
    demographic_data['race'] = member.race
    demographic_data['marital_status'] = member.member[0].marital_status
    demographic_data['education'] = member.member[0].education
    demographic_data['english_proficiency'] = member.member[0].english_proficiency
    demographic_data['english_reading_level'] = member.member[0].english_reading_level
    demographic_data['english_writing_level'] = member.member[0].english_writing_level
    demographic_data['employment_status'] = member.member[0].employment_status
    demographic_data['income'] = member.member[0].income
    demographic_data['income_sources'] = []
    for entry in member.member[0].income_sources:
        demographic_data['income_sources'].append(entry.income_source)
    demographic_data['assets'] = []
    for entry in member.member[0].assets:
        demographic_data['assets'].append(entry.asset)
    demographic_data['has_car'] = member.member[0].has_car
    demographic_data['has_health_insurance'] = member.member[0].has_health_insurance
    demographic_data['has_primary_care_doctor'] = member.member[0].has_primary_care_doctor
    demographic_data['medical_issues'] = []
    for entry in member.member[0].medical_issues:
        demographic_data['medical_issues'].append(entry.medical_issue)
    demographic_data['enrolled_in_military'] = member.member[0].enrolled_in_military
    demographic_data['has_served_in_military'] = member.member[0].has_served_in_military
    demographic_data['wars_served'] = []
    for entry in member.member[0].wars_served:
        demographic_data['wars_served'].append(entry.war_served)
    return demographic_data

'''
Get the self sufficiency matrices for a member to put into the member modal
'''
def getSelfSufficiencyMatrix(username):
    member = models.User.query.get(username)
    self_sufficiency_matrix = {}
    for entry in member.member[0].self_sufficiency_matrices:
        date = datetime.strftime(entry.assessment_date, '%Y-%m-%d')
        self_sufficiency_matrix[date] = {}
        entry_items = entry.__dict__
        for key, value in entry_items.items():
            if key != 'assessment_date' and key != '_sa_instance_state' and key != 'username':
                self_sufficiency_matrix[date][key] = str(value)
    return self_sufficiency_matrix

'''
Get the self efficacy quizzes for a member to put into the member modal
'''
def getSelfEfficacyQuiz(username):
    member = models.User.query.get(username)
    self_efficacy_quiz = {}
    for entry in member.member[0].self_efficacy_quizzes:
        date = datetime.strftime(entry.assessment_date, '%Y-%m-%d')
        self_efficacy_quiz[date] = {}
        entry_items = entry.__dict__
        for key, value in entry_items.items():
            if key != 'assessment_date' and key != '_sa_instance_state' and key != 'username':
                self_efficacy_quiz[date][key] = str(value)
    return self_efficacy_quiz