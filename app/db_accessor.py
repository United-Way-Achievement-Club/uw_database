'''
Title
-----
db_accessor.py

Description
-----------
Retrieve and add items to the database

'''
from app import db, models

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
    return models.Member.query.all()

'''
Get member by username
'''
def getMember(username):
    member = models.User.query.join(models.Member).filter_by(username=username).first()
    return member

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