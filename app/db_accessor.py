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
from sqlalchemy.orm import class_mapper, ColumnProperty


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
Update a user after edit profile
'''
def updateUser(user_data, username):
    user = models.User.query.get(username)
    user.birth_date = datetime.strptime(user_data['birth_date'], '%Y-%m-%d')
    user.address_street = user_data['address_street']
    user.address_state = user_data['address_state']
    user.address_city = user_data['address_city']
    user.address_zip = user_data['address_zip']
    user.email = user_data['email']
    old_phones = models.User_Phone.query.filter_by(username=username)
    for number in old_phones:
        if number.phone in user_data['phone_numbers']:
            index = user_data['phone_numbers'].index(number.phone)
            del user_data['phone_numbers'][index]
        else:
            models.User_Phone.query.filter_by(username=username, phone=number.phone).delete()
    for phone in user_data['phone_numbers']:
        db.session.add(models.User_Phone(username=username, phone=phone))
    db.session.commit()

'''
Get member phone numbers by username
'''
def getPhoneNumbers(username):
    phone_numbers = models.User_Phone.query.filter_by(username=username).all()
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
    return models.User.query.filter_by(type='coordinator').all()

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
    
    #handle other_race logic for insertion later
    if demographic_data['race']=='other':
        user_race = demographic_data['other_race']
    else:
        user_race = demographic_data['race']
    
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
                                                birth_date = datetime.strptime(enrollment_form['birth_date'], "%Y-%m-%d")
                                                )
                          )
    
    db.session.add(models.Member( username = general['username'],
                                                    join_date = datetime.strptime(general['join_date'], "%Y-%m-%d"),
                                                    club_name = general['club_name'],
                                                    commitment_pledge = datetime.strptime(general['commitment_pledge'], "%Y-%m-%d"),
                                                    photo_release = datetime.strptime(general['photo_release'], "%Y-%m-%d"),
                                                    education = demographic_data['education'],
                                                    marital_status = demographic_data['marital_status'],
                                                    income = demographic_data['income'],
                                                    credit_score = int(demographic_data['credit_score']),
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
        db.session.add(models.User_Phone(  username = general['username'],
                                                                    phone = phone_number
                                                                 )
                              )
                                                                                     
    for item in demographic_data['medical_issues']:
        db.session.add(models.Member_Medical_Issues( username = general['username'],
                                                                                medical_issue = item.strip()
                                                                             )
                              )
                                                                                     
    for war in demographic_data['wars_served']:
        db.session.add(models.Member_Wars_Served(username = general['username'],
                                                                            war_served = war
                                                                            )
                              )
    
    for child in enrollment_form['children']:
        db.session.add(models.Child(  parent = general['username'],
                                                    child_first_name = child['child_first_name'],
                                                    child_last_name = child['child_last_name'],
                                                    child_birth_date = datetime.strptime(child['child_birth_date'], "%Y-%m-%d"),
                                                    child_gender = child['child_gender'],
                                                    child_grade_level = child['child_grade_level'],
                                                    child_grades = child['child_grades'],
                                                    child_school = child['child_school']
                                                  )
                               )
    
    for date in self_sufficiency_matrix:
        db.session.add(models.Member_Self_Sufficiency_Matrix( username = general['username'],
                                                                                            assessment_date = datetime.strptime(date, "%Y-%m-%d"),
                                                                                            housing = self_sufficiency_matrix[date]['housing'],
                                                                                            employment = self_sufficiency_matrix[date]['employment'],
                                                                                            income = self_sufficiency_matrix[date]['income'],
                                                                                            food = self_sufficiency_matrix[date]['food'],
                                                                                            child_care = self_sufficiency_matrix[date]['child_care'],
                                                                                            childrens_education = self_sufficiency_matrix[date]['childrens_education'],
                                                                                            adult_education = self_sufficiency_matrix[date]['adult_education'],
                                                                                            health_care_coverage = self_sufficiency_matrix[date]['health_care_coverage'],
                                                                                            life_skills = self_sufficiency_matrix[date]['life_skills'],
                                                                                            family_social_relations = self_sufficiency_matrix[date]['family_social_relations'],
                                                                                            mobility = self_sufficiency_matrix[date]['mobility'],
                                                                                            community_involvement = self_sufficiency_matrix[date]['community_involvement'],
                                                                                            parenting_skills = self_sufficiency_matrix[date]['parenting_skills'],
                                                                                            legal = self_sufficiency_matrix[date]['legal'],
                                                                                            mental_health = self_sufficiency_matrix[date]['mental_health'],
                                                                                            substance_abuse = self_sufficiency_matrix[date]['substance_abuse'],
                                                                                            safety = self_sufficiency_matrix[date]['safety'],
                                                                                            disabilities = self_sufficiency_matrix[date]['disabilities'],
                                                                                            other = self_sufficiency_matrix[date]['other']
                                                                                            )

                              )
    
    for date in self_efficacy_quiz:
        db.session.add(models.Member_Self_Efficacy_Quiz( username = general['username'],
                                                                                    assesment_date = datetime.strptime(date, "%Y-%m-%d"),
                                                                                    self_efficacy_1 = self_efficacy_quiz[date]['self_efficacy_1'],
                                                                                    self_efficacy_2 = self_efficacy_quiz[date]['self_efficacy_2'],
                                                                                    self_efficacy_3 = self_efficacy_quiz[date]['self_efficacy_3'],
                                                                                    self_efficacy_4 = self_efficacy_quiz[date]['self_efficacy_4'],
                                                                                    self_efficacy_5 = self_efficacy_quiz[date]['self_efficacy_5'],
                                                                                    self_efficacy_6 = self_efficacy_quiz[date]['self_efficacy_6'],
                                                                                    self_efficacy_7 = self_efficacy_quiz[date]['self_efficacy_7'],
                                                                                    self_efficacy_8 = self_efficacy_quiz[date]['self_efficacy_8'],
                                                                                    self_efficacy_9 = self_efficacy_quiz[date]['self_efficacy_9'],
                                                                                    self_efficacy_10 = self_efficacy_quiz[date]['self_efficacy_10'],
                                                                                    self_efficacy_11 = self_efficacy_quiz[date]['self_efficacy_11'],
                                                                                    self_efficacy_12 = self_efficacy_quiz[date]['self_efficacy_12']
                                                                                    )
                              )
    
    db.session.commit()

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
    general = updated_member['general']
    old_general = old_member['general']
    
    enrollment_form = updated_member['enrollment_form']
    old_enrollment_form = old_member['enrollment_form']
    
    demographic_data = updated_member['demographic_data']
    old_demographic_data = old_member['demographic_data']
    
    self_sufficiency_matrices = updated_member['self_sufficiency_matrix']
    old_self_sufficiency_matrices = old_member['self_sufficiency_matrix']
    
    self_efficacy_quizzes = updated_member['self_efficacy_quiz']
    old_self_efficacy_quizzes = old_member['self_efficacy_quiz']
    
    user=models.User.query.filter_by(username=old_general['username']).first()
    member=models.User.query.filter_by(username=old_general['username']).first()
    
    if general['password'] != old_general['password']:
        user.password=general['password']
    if enrollment_form['first_name'] != old_enrollment_form['first_name']:
        user.first_name = enrollment_form['first_name']
    if enrollment_form['last_name'] != old_enrollment_form['last_name']:
        user.last_name = enrollment_form['last_name']
    if enrollment_form['email'] != old_enrollment_form['email']:
        user.email = enrollment_form['email']
    if demographic_data['race'] == 'other':
        if demographic_data['other_race'] != old_demographic_data['other_race']:
            user.race = demographic_data['other_race']
    elif demographic_data['race'] != old_demographic_data['race']:
        user.race = demographic_data['race']
    if enrollment_form['address_street'] != old_enrollment_form['address_street']:
        user.address_street = enrollment_form['address_street']
    if enrollment_form['address_city'] != old_enrollment_form['address_city']:
        user.address_city = enrollment_form['address_city']
    if enrollment_form['address_state'] != old_enrollment_form['address_state']:
        user.address_state = enrollment_form['address_state']
    if enrollment_form['address_zip'] != old_enrollment_form['address_zip']:
        user.address_zip = enrollment_form['address_zip']
    if enrollment_form['birth_date'] != old_enrollment_form['birth_date']:
        user.birth_date = datetime.strptime(enrollment_form['birth_date'], "%Y-%m-%d")
        
    if general['join_date'] != old_general['join_date']:
        user.member[0].join_date = datetime.strptime(general['join_date'], "%Y-%m-%d")
    if general['club_name'] != old_general['club_name']:
        user.member[0].club_name = general['club_name']
    if general['commitment_pledge'] != old_general['commitment_pledge']:
        user.member[0].commitment_pledge = datetime.strptime(general['commitment_pledge'], "%Y-%m-%d")
    if general['photo_release'] != old_general['photo_release']:
        user.member[0].photo_release = datetime.strptime(general['photo_release'], "%Y-%m-%d")
    if demographic_data['education'] != old_demographic_data['education']:
        user.member[0].education = demographic_data['education']
    if demographic_data['marital_status'] != old_demographic_data['marital_status']:
        user.member[0].marital_status = demographic_data['marital_status']
    if demographic_data['income'] != old_demographic_data['income']:
        user.member[0].income = demographic_data['income']
    if demographic_data['credit_score'] == '':
        demographic_data['credit_score'] = None
    if demographic_data['credit_score'] != old_demographic_data['credit_score']:
        user.member[0].credit_score = int(demographic_data['credit_score'])
    if demographic_data['employment_status'] != old_demographic_data['employment_status']:
        user.member[0].employment_status = demographic_data['employment_status']
        #keyError with referral_source.
    # if enrollment_form['referral_source'] != old_enrollment_form['referral_source']:
        # user.member[0].referral_source = enrollment_form['referral_source']
    if enrollment_form['spouse_first_name'] != old_enrollment_form['spouse_first_name']:
        user.member[0].spouse_first_name = enrollment_form['spouse_first_name']
    if enrollment_form['spouse_last_name'] != old_enrollment_form['spouse_last_name']:
        user.member[0].spouse_last_name = enrollment_form['spouse_last_name']
    if demographic_data['english_proficiency'] != old_demographic_data['english_proficiency']:
        user.member[0].english_proficiency = demographic_data['english_proficiency']
    if demographic_data['english_reading_level'] != old_demographic_data['english_reading_level']:
        user.member[0].english_reading_level = demographic_data['english_reading_level']
    if demographic_data['english_writing_level'] != old_demographic_data['english_writing_level']:
        user.member[0].english_writing_level = demographic_data['english_writing_level']
    if demographic_data['has_car'] != old_demographic_data['has_car']:
        user.member[0].has_car = demographic_data['has_car']
    if 'has_health_insurance' in demographic_data and demographic_data['has_health_insurance'] != old_demographic_data['has_health_insurance']:
        user.member[0].has_health_insurance = demographic_data['has_health_insurance']
    if 'has_primary_care_doctor' in demographic_data and demographic_data['has_primary_care_doctor'] != old_demographic_data['has_primary_care_doctor']:
        user.member[0].has_primary_care_doctor = demographic_data['has_primary_care_doctor']
    if 'enrolled_in_military' in demographic_data and demographic_data['enrolled_in_military'] != old_demographic_data['enrolled_in_military']:
        user.member[0].enrolled_in_military = demographic_data['enrolled_in_military']
    if 'has_served_in_military' in demographic_data and demographic_data['has_served_in_military'] != old_demographic_data['has_served_in_military']:
        user.member[0].has_served_in_military = demographic_data['has_served_in_military']
    
    for income_source in user.member[0].income_sources:
        if income_source.income_source not in demographic_data['income_sources']:
            db.session.delete(income_source)
    for item in demographic_data['income_sources']:
        if item not in old_demographic_data['income_sources']:
            db.session.add(models.Member_Sources_Of_Income(username = old_general['username'], income_source = item))
    
    for asset in user.member[0].assets:
        if asset.asset not in demographic_data['assets']:
            db.session.delete(asset)
    for item in demographic_data['assets']:
        if item not in old_demographic_data['assets']:
            db.session.add(models.Member_Assets(username = old_general['username'], asset = item))
            
    for number in user.phone_numbers:
        if number.phone not in enrollment_form['phone_numbers']:
            db.session.delete(number)
    for item in enrollment_form['phone_numbers']:
        if item not in old_enrollment_form['phone_numbers']:
            db.session.add(models.User_Phone(username = old_general['username'], phone = item))
    
    for issue in user.member[0].medical_issues:
        if issue.medical_issue not in demographic_data['medical_issues']:
            db.session.delete(issue)
    for item in demographic_data['medical_issues']:
        if item not in old_demographic_data['medical_issues']:
            db.session.add(models.Member_Medical_Issues(username = old_general['username'], medical_issue = item))
    
    for war in user.member[0].wars_served:
        if war.war_served not in demographic_data['wars_served']:
            db.session.delete(war)
    for item in demographic_data['wars_served']:
        if item not in old_demographic_data['wars_served']:
            db.session.add(models.Member_Wars_Served(username = old_general['username'], war_served = item))
        
    for matrix in user.member[0].self_sufficiency_matrices:
        db.session.delete(matrix)
    for date in self_sufficiency_matrices:
        db.session.add(models.Member_Self_Sufficiency_Matrix( username = old_general['username'],
                                                                                            assessment_date = datetime.strptime(date, "%Y-%m-%d"),
                                                                                            housing = self_sufficiency_matrices[date]['housing'],
                                                                                            employment = self_sufficiency_matrices[date]['employment'],
                                                                                            income = self_sufficiency_matrices[date]['income'],
                                                                                            food = self_sufficiency_matrices[date]['food'],
                                                                                            child_care = self_sufficiency_matrices[date]['child_care'],
                                                                                            childrens_education = self_sufficiency_matrices[date]['childrens_education'],
                                                                                            adult_education = self_sufficiency_matrices[date]['adult_education'],
                                                                                            health_care_coverage = self_sufficiency_matrices[date]['health_care_coverage'],
                                                                                            life_skills = self_sufficiency_matrices[date]['life_skills'],
                                                                                            family_social_relations = self_sufficiency_matrices[date]['family_social_relations'],
                                                                                            mobility = self_sufficiency_matrices[date]['mobility'],
                                                                                            community_involvement = self_sufficiency_matrices[date]['community_involvement'],
                                                                                            parenting_skills = self_sufficiency_matrices[date]['parenting_skills'],
                                                                                            legal = self_sufficiency_matrices[date]['legal'],
                                                                                            mental_health = self_sufficiency_matrices[date]['mental_health'],
                                                                                            substance_abuse = self_sufficiency_matrices[date]['substance_abuse'],
                                                                                            safety = self_sufficiency_matrices[date]['safety'],
                                                                                            disabilities = self_sufficiency_matrices[date]['disabilities'],
                                                                                            other = self_sufficiency_matrices[date]['other']
                                                                                            ))

    for quiz in user.member[0].self_efficacy_quizzes:
        db.session.delete(quiz)
    for date in self_efficacy_quizzes:
        db.session.add(models.Member_Self_Efficacy_Quiz( username = old_general['username'],
                                                                                    assesment_date = datetime.strptime(date, "%Y-%m-%d"),
                                                                                    self_efficacy_1 = self_efficacy_quizzes[date]['self_efficacy_1'],
                                                                                    self_efficacy_2 = self_efficacy_quizzes[date]['self_efficacy_2'],
                                                                                    self_efficacy_3 = self_efficacy_quizzes[date]['self_efficacy_3'],
                                                                                    self_efficacy_4 = self_efficacy_quizzes[date]['self_efficacy_4'],
                                                                                    self_efficacy_5 = self_efficacy_quizzes[date]['self_efficacy_5'],
                                                                                    self_efficacy_6 = self_efficacy_quizzes[date]['self_efficacy_6'],
                                                                                    self_efficacy_7 = self_efficacy_quizzes[date]['self_efficacy_7'],
                                                                                    self_efficacy_8 = self_efficacy_quizzes[date]['self_efficacy_8'],
                                                                                    self_efficacy_9 = self_efficacy_quizzes[date]['self_efficacy_9'],
                                                                                    self_efficacy_10 = self_efficacy_quizzes[date]['self_efficacy_10'],
                                                                                    self_efficacy_11 = self_efficacy_quizzes[date]['self_efficacy_11'],
                                                                                    self_efficacy_12 = self_efficacy_quizzes[date]['self_efficacy_12']
                                                                                    ))
                                                                                    
    db.session.commit()


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
    for entry in member.phone_numbers:
        enrollment_form['phone_numbers'].append(entry.phone)
    enrollment_form['spouse_first_name'] = member.member[0].spouse_first_name
    enrollment_form['spouse_last_name'] = member.member[0].spouse_last_name
    enrollment_form['children'] = []
    for entry in children:
        child_obj = {}
        child_obj['child_first_name'] = entry.child_first_name
        child_obj['child_last_name'] = entry.child_last_name
        child_obj['child_gender'] = entry.child_gender
        child_obj['child_birth_date'] = datetime.strftime(entry.child_birth_date, '%Y-%m-%d')
        child_obj['child_school'] = entry.child_school
        child_obj['child_grade_level'] = entry.child_grade_level
        child_obj['child_grades'] = entry.child_grades
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
    demographic_data['credit_score'] = member.member[0].credit_score
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

'''
Add new goal to the database
'''
def addGoal(goal):
    goal_dict = goal
    goal_record = models.Goals( goal_name = goal_dict['goal_name'],
                                goal_category = goal_dict['goal_category'],
                                description = 'none',
                                num_of_steps = 3
                                )
    db.session.add(goal_record)
    
    step1 = models.Steps(step_name = goal_dict['steps'][0]['step_name'],
                        goal_name = goal_dict['goal_name'],
                        description = 'none',
                        step_num = 1,
                        num_of_proofs = len(goal_dict['steps'][0]['proofs'])
                        )
    db.session.add(step1)
    
    step2 = models.Steps(step_name = goal_dict['steps'][1]['step_name'],
                        goal_name = goal_dict['goal_name'],
                        description = 'none',
                        step_num = 2,
                        num_of_proofs = len(goal_dict['steps'][1]['proofs'])
                        )
    db.session.add(step2)
                        
    step3 = models.Steps(step_name = goal_dict['steps'][2]['step_name'],
                        goal_name = goal_dict['goal_name'],
                        description = 'none',
                        step_num = 3,
                        num_of_proofs = len(goal_dict['steps'][2]['proofs'])
                        )
    db.session.add(step3)
                        
    for i in range(0,len(goal_dict['steps'])):
        for j in range(0,len(goal_dict['steps'][i]['proofs'])):
            proof = models.Proof(   proof_name = goal_dict['steps'][i]['proofs'][j]['proof_document'],
                                    step_name = goal_dict['steps'][i]['step_name'],
                                    description = goal_dict['steps'][i]['proofs'][j]['proof_description'],
                                    proof_num = j+1
                                    )
            db.session.add(proof)
            
    db.session.commit()