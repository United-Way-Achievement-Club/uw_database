'''
Title
------
utils.py

Description
------------
Helper methods that are used to parse data

'''

import datetime
import re

'''
Validate member object, check if all required fields
are completed and in the correct format
'''
def validateMember(memberObj):
    print memberObj
    # validate general
    general = validateGeneral(memberObj['general'])
    if general["success"] == False:
        return general
    # validate enrollment form
    enrollment_form = validateEnrollmentForm(memberObj['enrollment_form'])
    if enrollment_form["success"] == False:
        return enrollment_form
    # validate demographic data
    demographic_data = validateDemographicData(memberObj['demographic_data'])
    if demographic_data["success"] == False:
        return demographic_data
    # validate self sufficiency matrix
    self_sufficiency_matrix = validateSelfSufficiencyMatrix(memberObj['self_sufficiency_matrix'])
    if self_sufficiency_matrix["success"] == False:
        return self_sufficiency_matrix
    # validate self efficacy quiz
    self_efficacy_quiz = validateSelfEfficacyQuiz(memberObj['self_efficacy_quiz'])
    if self_efficacy_quiz["success"] == False:
        return self_efficacy_quiz
    return {"success":True, "error":None}

'''
Validate general portion of member object
'''
def validateGeneral(general):
    date_string = "%Y-%m-%d"
    if general == {}:
        return {"success":False, "error":"general form must be filled out"}
    if general['username'] == '':
        return {"success":False, "error":"Username can not be blank"}
    elif len(general['username']) < 5:
        return {"success":False, "error":"Username must be greater than 5 characters"}
    elif len(general['password']) < 8:
        return {"success":False, "error":"Password must be 8 or more characters"}
    # TODO: check club name against clubs in database as well
    elif general['club_name'] == '':
        return {"success":False, "error":"Club Name must not be blank"}
    elif general['join_date'] == '':
        return {"success":False, "error":"Must select join date"}
    elif datetime.datetime.strptime(general['join_date'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Join date must not be in the future"}
    elif general['photo_release'] == '':
        return {"success":False, "error":"Must select date for Photo Release Signature"}
    elif datetime.datetime.strptime(general['photo_release'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Photo Release sign date must not be in the future"}
    elif general['commitment_pledge'] == '':
        return {"success":False, "error":"Must select date for Commitment Pledge Signature"}
    elif datetime.datetime.strptime(general['commitment_pledge'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Commitment Pledge sign date must not be in the future"}
    return {"success":True, "error":None}

'''
Validate enrollment form portion of member object
'''
def validateEnrollmentForm(enrollment_form):
    date_string = "%Y-%m-%d"
    if enrollment_form == {}:
        return {"success":False, "error":"Enrollment form must be filled out"}
    elif enrollment_form['first_name'] == '':
        return {"success":False, "error":"Member must have a first name"}
    elif enrollment_form['last_name'] == '':
        return {"success":False, "error":"Member must have a last name"}
    elif enrollment_form['address_street'] == '':
        return {"success":False, "error":"Address street name can not be blank"}
    elif enrollment_form['address_city'] == '':
        return {"success":False, "error":"Address city can not be blank"}
    elif enrollment_form['address_zip'] == '':
        return {"success":False, "error":"Address zip code can not be blank"}
    elif not re.match('^\d{5}(?:[-\s]\d{4})?$', enrollment_form['address_zip']):
        return {"success":False, "error":"Invalid Zip Code"}
    elif enrollment_form['birth_date'] == '':
        return {"success":False, "error":"Birth Date must not be blank"}
    elif datetime.datetime.strptime(enrollment_form['birth_date'], date_string) > datetime.datetime.now():
        return {"success":False, "error":"Birth date must not be in the future"}
    elif enrollment_form['phone_numbers'][0] == '' and len(enrollment_form['phone_numbers']) == 1:
        return {"success":False, "error":"Must include at least 1 phone number"}
    elif enrollment_form['email'] != '' and not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', enrollment_form['email']):
        return {"success":False, "error":"Invalid email address"}
    for number in enrollment_form['phone_numbers']:
        if not re.match('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', number):
            return {"success":False, "error":"Phone numbers must be in a valid format"}
    for child in enrollment_form['children']:
        if child['child_first_name'] == '':
            return {"success":False, "error":"Child first name must not be blank"}
        elif child['child_last_name'] == '':
            return {"success":False, "error":"Child last name must not be blank"}
        elif child['child_birth_date'] == '':
            return {"success":False, "error":"Child birth date must not be blank"}
    return {"success":True, "error":None}


'''
Validate demographic data portion of member object
'''
def validateDemographicData(demographic_data):
    return {"success":True, "error":None}

'''
Validate self sufficiency matrix portion of member object
'''
def validateSelfSufficiencyMatrix(self_sufficiency_matrix):
    return {"success":True, "error":None}

'''
Validate self efficacy quiz portion of member object
'''
def validateSelfEfficacyQuiz(self_efficacy_quiz):
    return {"success":True, "error":None}

def getStates():
    return ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]