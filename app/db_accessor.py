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
Return all of the coordinators in the database
'''
def getCoordinators():
    return models.Coordinator.query.all()

'''
Add a new member to the database
'''
def addMember(member_obj):
    general = member_obj['general']
    enrollment_form = member_obj['enrollment_form']
    demographic_data = member_obj['demographic_data']
    self_sufficiency_matrix = member_obj['self_sufficiency_matrix']
    self_efficacy_quiz = member_obj['self_efficacy_quiz']
    # TODO: parse values from these objects and create a new member based on them
    # db.session.add(models.User(username=username ...))
    # db.session.add(models.Member(username=username ...))
    # db.session.commit()