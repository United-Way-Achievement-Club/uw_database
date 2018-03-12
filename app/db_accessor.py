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

    #temp code to learn the keys of the dicts I'm working with
    # print 'general'
    # print member_obj['general'].keys()
    # print 'enrollment_form'
    # print member_obj['enrollment_form'].keys()
    # print 'demographic_data'
    # print member_obj['demographic_data']['income_sources']
    # print 'self_sufficiency_matrix'
    # print self_sufficiency_matrix
    # print 'self_efficacy_quiz'
    # print member_obj['self_efficacy_quiz'][member_obj['self_efficacy_quiz'].keys()[0]]
        
    
    # TODO: parse values from these dictionaries and create a new member based on them
    # first, db.session.add(models.User(username=username ...))
    
    #handle other_race logic for insertion later
    if demographic_data['race']=='other':
        user_race = demographic_data['other_race']
    else:
        user_race = demographic_data['race']
        
    # add form data to User table
    db.session.add(models.User(  username = general['username'],
                                                type = 'member',
                                                password = general['password'],
                                                profile_picture = general['profile_picture'],
                                                first_name = enrollment_form['first_name'],
                                                last_name = enrollment_form['last_name'],
                                                email = enrollment_form['email'],
                                                gender = demographic_data['gender'],
                                                race = user_race,
                                                address_street = enrollment_form['address_street'],
                                                address_city = enrollment_form['address_city'],
                                                address_state = enrollment_form['address_state'],
                                                county = 'null',
                                                address_zip = enrollment_form['address_zip'],
                                                birth_date = enrollment_form['birth_date']
                                                )
                          )

    # then, db.session.add(models.Member(username=username ...))
    db.session.add(models.Member( username = general['username'],
                                                    join_date = general['join_date'],
                                                    club_name = general['club_name'],
                                                    commitment_pledge = general['commitment_pledge'],
                                                    photo_release = general['photo_release'],
                                                    education = demographic_data['education'],
                                                    marital_status = demographic_data['marital_status'],
                                                    income = demographic_data['income'],
                                                    credit_score = demographic_data['credit_score'],
                                                    employment_status = demographic_data['employment_status'],
                                                    referral_source = enrollment_form['referral_source'],
                                                    spouse_first_name = enrollment_form['spouse_first_name'],
                                                    spouse_last_name = enrollment_form['spouse_last_name'],
                                                    english_proficiency = demographic_data['english_proficiency'],
                                                    english_reading_level = demographic_data['english_reading_level'],
                                                    english_writing_level = demographic_data['english_writing_level'],
                                                    has_car = demographic_data['has_car'],
                                                    has_health_insurance = demographic_data['has_health_insurance'],
                                                    has_primary_care_doctor = demographic_data['has_primary_care_doctor'],
                                                    enrolled_in_military = demographic_data['enrolled_in_military'],
                                                    has_served_in_military = demographic_data['has_served_in_military']
                                                    )
                          )
    
    for item in demographic_data['income_sources']:
        db.session.add(models.Member_Sources_Of_Income(  username = general['username'],
                                                                                        income_source = item
                                                                                     )
                              )
                                                                                     
    for asset in demographic_data['assets']:
        db.session.add(models.Member_Assets(  username = general['username'],
                                                                    asset = asset
                                                                    )
                              )
                                                                                     
    for phone_number in enrollment_form['phone_numbers']:
        db.session.add(models.Member_Phone(  username = general['username'],
                                                                    phone = phone_number
                                                                 )
                              )
                                                                                     
    #edit to handle new front end array jibbajabba
    # for line in demographic_data['medical_issues']:
        # db.session.add(models.Member_Medical_Issues(  username = general['username'],
                                                                                        # issue = line
                                                                                     # )
                                 # )
                                                                                     
    for war in demographic_data['wars_served']:
        db.session.add(models.Member_Wars_Served(username = general['username'],
                                                                            war_served = war
                                                                            )
                              )
    
    for child in enrollment_form['children']:
        db.session.add(models.Child(  parent = general['username'],
                                                    first_name = child['child_first_name'],
                                                    last_name = child['child_last_name'],
                                                    birth_date = child['child_birth_date'],
                                                    gender = child['child_gender'],
                                                    grade_level = child['child_grade_level'],
                                                    grades = child['child_grades'],
                                                    school = child['child_school']
                                                  )
                               )
    
    # add to Member_Self_Sufficiency_Matrix
    for date in self_sufficiency_matrix:
        db.session.add(models.Member_Self_Sufficiency_Matrix( username = general['username'],
                                                                                            assesment_date = datetime.datetime(int(date[:date.find('-')]),int(date[date.find('-')+1:date.find('-',date.find('-')+1)]),int(date[date.rfind('-')+1:])),
                                                                                            housing = int(self_sufficiency_matrix[date]['housing']),
                                                                                            employment = int(self_sufficiency_matrix[date]['employment']),
                                                                                            income = int(self_sufficiency_matrix[date]['income']),
                                                                                            food = int(self_sufficiency_matrix[date]['food']),
                                                                                            child_care = int(self_sufficiency_matrix[date]['child_care']),
                                                                                            childrens_education = int(self_sufficiency_matrix[date]['childrens_education']),
                                                                                            adult_education = int(self_sufficiency_matrix[date]['adult_education']),
                                                                                            health_care_coverage = int(self_sufficiency_matrix[date]['health_care_coverage']),
                                                                                            life_skills = int(self_sufficiency_matrix[date]['life_skills']),
                                                                                            family_social_relations = int(self_sufficiency_matrix[date]['family_social_relations']),
                                                                                            mobility = int(self_sufficiency_matrix[date]['mobility']),
                                                                                            community_involvement = int(self_sufficiency_matrix[date]['community_involvement']),
                                                                                            parenting_skills = int(self_sufficiency_matrix[date]['parenting_skills']),
                                                                                            legal = int(self_sufficiency_matrix[date]['legal']),
                                                                                            mental_health = int(self_sufficiency_matrix[date]['mental_health']),
                                                                                            substance_abuse = int(self_sufficiency_matrix[date]['substance_abuse']),
                                                                                            safety = int(self_sufficiency_matrix[date]['safety']),
                                                                                            disabilities = int(self_sufficiency_matrix[date]['disabilities']),
                                                                                            other = int(self_sufficiency_matrix[date]['other'])
                                                                                            )

                              )
    
    # add to Member_Self_Efficacy_Quiz
    for date in self_efficacy_quiz:
        db.session.add(models.Member_Self_Efficacy_Quiz( username = general['username']
                                                                                    assesment_date = datetime.datetime(int(date[:date.find('-')]),int(date[date.find('-')+1:date.find('-',date.find('-')+1)]),int(date[date.rfind('-')+1:])),
                                                                                    question_1 = int(self_efficacy_quiz[date]['self_efficacy_1']),
                                                                                    question_2 = int(self_efficacy_quiz[date]['self_efficacy_2']),
                                                                                    question_3 = int(self_efficacy_quiz[date]['self_efficacy_3']),
                                                                                    question_4 = int(self_efficacy_quiz[date]['self_efficacy_4']),
                                                                                    question_5 = int(self_efficacy_quiz[date]['self_efficacy_5']),
                                                                                    question_6 = int(self_efficacy_quiz[date]['self_efficacy_6']),
                                                                                    question_7 = int(self_efficacy_quiz[date]['self_efficacy_7']),
                                                                                    question_8 = int(self_efficacy_quiz[date]['self_efficacy_8']),
                                                                                    question_9 = int(self_efficacy_quiz[date]['self_efficacy_9']),
                                                                                    question_10 = int(self_efficacy_quiz[date]['self_efficacy_10']),
                                                                                    question_11 = int(self_efficacy_quiz[date]['self_efficacy_11']),
                                                                                    question_12 = int(self_efficacy_quiz[date]['self_efficacy_12'])
                                                                                    )
                              )
    
    db.session.commit()