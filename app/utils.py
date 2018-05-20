'''
Title
------
utils.py

Description
------------
Helper methods

'''

import datetime
import re

import requests
import json

# temporary clubs object
global clubs
clubs = [
    {
        "club_name":"Atlanta High School",
        "address_street": "1225 Caroline St NE",
        "address_city": "Atlanta",
        "address_state": "GA",
        "address_zip": "30307",
        "county": "Fulton",
        "own_club": False,
        "num_members": 40,
        "num_coordinators": 3
    },
    {
        "club_name":"Georgia Institute of Technology",
        "address_street": "266 Ferst Dr NW",
        "address_city": "Atlanta",
        "address_state": "GA",
        "address_zip": "30332",
        "county": "Fulton",
        "own_club": False,
        "num_members": 35,
        "num_coordinators": 2
    },
    {
        "club_name":"United Way of Greater Atlanta",
        "address_street": "40 Courtland St NE #300",
        "address_city": "Atlanta",
        "address_state": "GA",
        "address_zip": "30303",
        "county": "Fulton",
        "own_club": False,
        "num_members": 24,
        "num_coordinators": 1
    },
    {
        "club_name":"Pebblebrook High School",
        "address_street": "991 Old Alabama Rd SW",
        "address_city": "Mableton",
        "address_state": "GA",
        "address_zip": "30126",
        "county": "Cobb",
        "own_club": True,
        "num_members": 27,
        "num_coordinators": 2
    }
]

# this is somewhat how a goals object should be structured when
# pulling from the database
goals = [
    {
        "goal_name": "Focus on my Child's Future",
        "category": "Education",
        "steps":
            [
                {
                    "step_name":"Be Active at Home",
                    "completed": True,
                    "current_step": False,
                    "proofs":
                        [
                            {"proof_name": "Copy of a reading log",
                             "proof_description": "Read to my child every night or have my child read to me every night for one month",
                             "document_name":"reading_log",
                             "completed": True,
                             "pending_approval": False,
                             "date":"3/1/18",
                             "document":"username_focus_on_my_childs_future_be_active_at_home_reading_log.pdf"},
                            {"proof_name":"Copy or a photo of the library cards",
                             "proof_description": "Get a library card for me and my child.",
                             "document_name": "library_card",
                             "completed": True,
                             "pending_approval": False,
                             "date":"3/1/18",
                             "document": "username_focus_on_my_childs_future_be_active_at_home_library_card.pdf"},
                            {"proof_name":"Copy or a photo of the homework.",
                             "proof_description": "Help my child with homework every night for a month",
                             "document_name":"homework",
                             "completed": True,
                             "pending_approval": False,
                             "date":"3/1/18",
                             "document": "username_focus_on_my_childs_future_be_active_at_home_homework.pdf"}
                        ]
                },
                {
                    "step_name":"Be Active at the School",
                    "completed": False,
                    "current_step": True,
                    "proofs":
                        [
                            {"proof_name": "Letter from the teacher on school letterhead",
                             "proof_description": "Attend a parent teacher conference",
                             "document_name":"teacher_letter",
                             "completed": True,
                             "pending_approval": False,
                             "date":"3/1/18",
                             "document":"username_focus_on_my_childs_future_be_active_at_school_teacher_letter.pdf"},
                            {"proof_name":"Letter from the volunteer leader",
                             "proof_description": "Volunteer at my child's school",
                             "document_name": "volunteer_leader_letter",
                             "completed": False,
                             "pending_approval": False,
                             "document": None},
                            {"proof_name":"Letter from the committee leader",
                             "proof_description": "Join a committee at my child's school",
                             "document_name":"committee_leader_letter",
                             "completed": True,
                             "pending_approval": False,
                             "date":"3/1/18",
                             "document": "username_focus_on_my_childs_future_be_active_at_school_committee_leader_letter.pdf"}
                        ]
                },
                {
                    "step_name":"Plan for the Future",
                    "completed": False,
                    "current_step": False,
                    "proofs":
                        [
                            {"proof_name": "Copy of your plan",
                             "proof_description": "Discover education requirements for my child's dream job. Make a plan for how they can meet these requirements.",
                             "document_name":"plan",
                             "completed": False,
                             "pending_approval": False,
                             "document": None},
                            {"proof_name":"Letter from the interviewee",
                             "proof_description": "Together, interview someone who works at your child's dream job.",
                             "document_name": "interviewee_letter",
                             "completed": False,
                             "pending_approval": False,
                             "document": None}
                        ]
                }
            ]
    }
]

'''
Return goals object
this function is temporary
until the database is set up
'''
def getTempGoals():
    return goals

'''
Return clubs object
This function is temporary until
the database is set up
It gets the latitude and longitude
once to map the locations
'''
def getTempClubs():
    global clubs
    for club in clubs:
        if 'latitude' not in club or 'longitude' not in club:
            results = getCoordinatesAndCounty(club['address_street'] + ' ' + club['address_city'] + ', ' + club['address_state'] + ' ' + club['address_zip'])
            club['latitude'] = results['latitude']
            club['longitude'] = results['longitude']
    print clubs
    return clubs

'''
Validate member object, check if all required fields
are completed and in the correct format
'''
def validateMember(memberObj, edit):
    # print memberObj
    # validate general
    general = validateGeneral(memberObj['general'], edit)
    general['form'] = 'general'
    if general["success"] == False:
        return general
    # validate enrollment form
    enrollment_form = validateEnrollmentForm(memberObj['enrollment_form'])
    enrollment_form['form'] = 'enrollment_form'
    if enrollment_form["success"] == False:
        return enrollment_form
    # validate demographic data
    demographic_data = validateDemographicData(memberObj['demographic_data'])
    demographic_data['form'] = 'demographic_data'
    if demographic_data["success"] == False:
        return demographic_data
    # validate self sufficiency matrix
    self_sufficiency_matrix = validateSelfSufficiencyMatrix(memberObj['self_sufficiency_matrix'])
    self_sufficiency_matrix['form'] = 'self_sufficiency_matrix'
    if self_sufficiency_matrix["success"] == False:
        return self_sufficiency_matrix
    # validate self efficacy quiz
    self_efficacy_quiz = validateSelfEfficacyQuiz(memberObj['self_efficacy_quiz'])
    self_efficacy_quiz['form'] = 'self_efficacy_quiz'
    if self_efficacy_quiz["success"] == False:
        return self_efficacy_quiz
    return {"success":True, "error":None}

'''
Validate general portion of member object
'''
def validateGeneral(general, edit):
    date_string = "%Y-%m-%d"
    if general == {}:
        return {"success":False, "error":"general form must be filled out"}
    if not edit and general['username'] == '':
        return {"success":False, "error":"Username can not be blank"}
    elif not edit and len(general['username']) < 5:
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
    if demographic_data == {}:
        return {"success":False, "error":"Demographic Data must be filled out"}
    if 'race' not in demographic_data:
        return {"success":False, "error":"Race is a required field"}
    if 'marital_status' not in demographic_data:
        return {"success":False, "error":"Marital Status is a required field"}
    if 'education' not in demographic_data:
        return {"success":False, "error":"Education is a required field"}
    if 'employment_status' not in demographic_data:
        return {"success":False, "error":"Employment is a required field"}
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

'''
Validate goal object
'''
def validateGoal(goal):
    # TODO: finish validate goal function
    for step in goal['steps']:
        if step['step_name'] == '':
            return {"success":False, "error":"Step Name can not be blank"}
    return {"success":True, "error":None}

'''
Validate club object
Check if the address is valid (can be geocoded)
'''
def validateClub(club):
    # TODO: finish validate club function
    if 'address_street' not in club:
        return {"success":False, "error":"Club must have street address", "club":None}
    club_address = club['address_street'] + ' ' + club['address_city'] + ', ' + club['address_state'] + ' ' + club['address_zip']
    coord = getCoordinatesAndCounty(club_address)
    if coord["success"] == False:
        return {"success":False, "error":"Invalid club address", "club":None}
    club['latitude'] = coord['latitude']
    club['longitude'] = coord['longitude']
    club['county'] = coord['county']
    return {"success":True, "error":None, "club":club}

'''
Return complete list of abbreviated US States
'''
def getStates():
    return ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

'''
Use the Google Geocoding API to get the location
and county of an address
'''
def getCoordinatesAndCounty(address):
    query_address_list = address.split(' ')
    query_address = '+'.join(query_address_list)
    apikey = 'AIzaSyAOZ9KV5NeXE2_Bw6G0Ot4OebKi1WSu3y4'
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + query_address + '&key=' + apikey)
    resp_json_payload = response.json()
    if len(resp_json_payload['results']) == 0:
        return {'latitude': None, 'longitude': None, 'county': None, 'success': False}
    lat = resp_json_payload['results'][0]['geometry']['location']['lat']
    long = resp_json_payload['results'][0]['geometry']['location']['lng']
    county = None
    for x in resp_json_payload['results'][0]['address_components']:
        if 'administrative_area_level_2' in x['types']:
            county = x['long_name']
    return {'latitude': lat, 'longitude': long, 'county': county, 'success': True}
