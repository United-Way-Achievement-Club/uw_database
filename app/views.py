'''
Title
-----
views.py

Description
-----------
Handle requests to the server by returning proper data or template

'''
from app import app
from db_accessor import *
from flask import render_template, redirect, session, request, jsonify, url_for
import json
from utils import validateMember, getStates, getTempGoals, validateGoal
import os


'''
If the member/coordinator isn't logged in, route to the login page
If not, route to the proper home page
'''
@app.route('/')
def index():
    if not session.get('login'):
        return redirect('login')
    else:
        member_type = session.get('member_type')
        if member_type == 'coordinator':
            return redirect('coordinator/home')
        else:
            return redirect('member/home')

'''
Render the login page
On POST, check if credentials are valid and redirect to proper home page
'''
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = loginUser(username, password)
        if user != None:
            session['login'] = True
            session['member_type'] = user.type
            member_type = user.type
            if member_type == 'coordinator':
                session['coordinator'] = user.username
                return redirect('coordinator/home')
            else:
                session['member'] = user.username
                return redirect('member/home')
    return render_template('login.html', error=False)

'''
Logout
'''
@app.route('/logout')
def logout():
    session['login'] = False
    session['member_type'] = None
    return redirect('login')

# ==================================================  MEMBER   =====================================================

'''
Route to the member home page if logged in
'''
@app.route('/member')
def member():
    if not session.get('login'):
        return redirect('login')
    else:
        return redirect('member/home')

# -- home --

'''
Member home page
'''
@app.route('/member/home')
def member_home():
    if not session.get('login'):
        return redirect('login')
    member = getMember(session.get('member'))
    phone_numbers = getPhoneNumbers(session.get('member'))
    return render_template('member/home.html', member=member, phone_numbers=phone_numbers, states=getStates())

'''
Edit the member's profile information
'''
@app.route('/member/edit_profile', methods=['POST'])
def member_edit_profile():
    if not session.get('login'):
        return redirect('login')
    member_data = json.loads(request.form['member_data'])
    username = session.get('member')
    updateUser(member_data, username)
    phone_numbers = getPhoneNumbers(session.get('member'))
    return render_template('member/home/profile.html', member=getMember(username), phone_numbers=phone_numbers, states=getStates())

'''
Edit the member's profile picture
'''
@app.route('/member/edit_profile_picture', methods=['POST'])
def member_edit_profile_picture():
    if not session.get('login'):
        return redirect('login')
    profile_picture = request.files['profile_picture']
    username = session.get('member')
    editProfilePic(username)
    phone_numbers = getPhoneNumbers(session.get('member'))
    profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], username + '.jpg'))
    return render_template('member/home/profile.html', member=getMember(username), phone_numbers=phone_numbers, states=getStates())

# -- goals --

'''
Member goals page
'''
@app.route('/member/goals')
def member_goals():
    if not session.get('login'):
        return redirect('login')
    username = session.get('member')
    return render_template('member/goals.html', member=getMember(username), goals=getTempGoals())


# ================================================= COORDINATOR ====================================================

'''
Route to the coordinator home page if logged in
'''
@app.route('/coordinator')
def coordinator():
    if not session.get('login'):
        return redirect('login')
    else:
        return redirect('coordinator/home')

# -- home --

'''
Coordinator home page
'''
@app.route('/coordinator/home')
def coordinator_home():
    if not session.get('login'):
        return redirect('login')
    phone_numbers = getPhoneNumbers(session.get('coordinator'))
    return render_template('coordinator/home.html', coordinator=getCoordinator(session.get('coordinator')), phone_numbers=phone_numbers, states=getStates())

'''
Edit the coordinator's profile information
'''
@app.route('/coordinator/edit_profile', methods=['POST'])
def coordinator_edit_profile():
    if not session.get('login'):
        return redirect('login')
    user_data = json.loads(request.form['user_data'])
    username = session.get('coordinator')
    updateUser(user_data, username)
    phone_numbers = getPhoneNumbers(session.get('coordinator'))
    return render_template('coordinator/home/profile.html', coordinator = getCoordinator(username), phone_numbers=phone_numbers, states=getStates())

'''
Edit the coordinator's profile picture
'''
@app.route('/coordinator/edit_profile_picture', methods=['POST'])
def coordinator_edit_profile_picture():
    if not session.get('login'):
        return redirect('login')
    profile_picture = request.files['profile_picture']
    username = session.get('coordinator')
    editProfilePic(username)
    phone_numbers = getPhoneNumbers(session.get('coordinator'))
    profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], username + '.jpg'))
    return render_template('coordinator/home/profile.html', coordinator = getCoordinator(username), phone_numbers=phone_numbers, states=getStates())

# -- goals --

'''
Coordinator goals page
'''
@app.route('/coordinator/goals')
def coordinator_goals():
    if not session.get('login'):
        return redirect('login')
    return render_template('coordinator/goals.html', coordinator = getCoordinator(session.get('coordinator')), goals=getGoals())

'''
Coordinator add a new goal to the database
First validate the goal (ensure the fields are
correct and that it doesn't already exist)
then add the goal to the database
'''
@app.route('/coordinator/goals/add_goal', methods=['POST'])
def coordinator_goals_add_goal():
    if not session.get('login'):
        return redirect('login')
    goal_obj = json.loads(request.form['goal'])

    # TODO: finish validateGoal in utils.py
    validation = validateGoal(goal_obj)
    if not validation['success']:
        return jsonify({"status_code":200, "message":validation['error'], "success":False})
        
    # TODO: database implement addGoal function in db_accessor.py
    addGoal(goal_obj)
    print goal_obj
    return jsonify({"status_code":200, "message":"Successfully added goal", "success":True})

# -- approve --

'''
Coordinator approve page
'''
@app.route('/coordinator/approve')
def coordinator_approve():
    if not session.get('login'):
        return redirect('login')
    return render_template('coordinator/approve.html', coordinator = getCoordinator(session.get('coordinator')))

# -- members --

'''
Coordinator members page
Query members from the database and send to template
'''
@app.route('/coordinator/members')
def coordinator_members():
    if not session.get('login'):
        return redirect('login')
    if not session.get('new_member'):
        session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
    if not session.get('modal_mode'):
        session['modal_mode'] = 'add'
    members = getMembers()

    return render_template('coordinator/members.html', members=members, coordinator = getCoordinator(session.get('coordinator')))

@app.route('/coordinator/members/edit', methods=['POST'])
def coordinator_members_edit():
    if not session.get('login'):
        return redirect('login')
    username = request.form['username']
    session['modal_mode'] = 'edit'
    session['edit_member'] = {'general':getGeneral(username), 'enrollment_form':getEnrollmentForm(username), 'demographic_data':getDemographicData(username), 'self_sufficiency_matrix':getSelfSufficiencyMatrix(username), 'self_efficacy_quiz':getSelfEfficacyQuiz(username)}
    session['old_edit_member'] = session.get('edit_member')
    return render_template('coordinator/members/add_member.html', member=session.get('edit_member'), initial_edit=True, disable_username=True)

'''
Update the current page in the add member modal
accept a key (the old page name), data(the data from the old page)
and the next page. Store the data from the old page in the
session temporarily, then redirect to the next page.
'''
@app.route('/coordinator/members/update', methods=['POST'])
def coordinator_members_update():
    if not session.get('login'):
        return redirect('login')
    print session.get('modal_mode')
    if session.get('modal_mode') == 'add':
        member_type = 'new_member'
        ext = ''
    elif session.get('modal_mode') == 'edit':
        member_type = 'edit_member'
        ext = 'edit_'
    member = session.get(member_type)
    key = request.form['key']
    data = request.form['data']
    if key != 'self_sufficiency_matrix' and key != 'self_efficacy_quiz':
        member[key] = json.loads(data)
        session[member_type] = member
    print session.get(member_type)
    next_page = ext + request.form['next_page']
    URL = 'coordinator_members_%s'%(next_page)
    return redirect(url_for(URL), code=307)

'''
Return the template for the general page in the add member modal
'''
@app.route('/coordinator/members/general', methods=['POST'])
def coordinator_members_general():
    if not session.get('login'):
        return redirect('login')
    view_member = session.get('new_member')['general']
    return render_template('coordinator/members/member_modal/general.html', view_member=view_member)

'''
Return the template for the general page in the add member modal for edit mode
'''
@app.route('/coordinator/members/edit/general', methods=['POST'])
def coordinator_members_edit_general():
    if not session.get('login'):
        return redirect('login')
    view_member = session.get('edit_member')['general']
    view_member['username'] = session.get('old_edit_member')['general']['username']
    return render_template('coordinator/members/member_modal/general.html', view_member=view_member, disable_username=True)

'''
Return the template for the enrollment form in the add member modal
'''
@app.route('/coordinator/members/enrollment_form', methods=['POST'])
def coordinator_members_enrollment_form():
    if not session.get('login'):
        return redirect('login')
    view_member = session.get('new_member')['enrollment_form']
    return render_template('coordinator/members/member_modal/enrollment_form.html', view_member=view_member, states=getStates())

'''
Return the template for the enrollment form in the add member modal in edit mode
'''
@app.route('/coordinator/members/edit/enrollment_form', methods=['POST'])
def coordinator_members_edit_enrollment_form():
    if not session.get('login'):
        return redirect('login')
    view_member = session.get('edit_member')['enrollment_form']
    return render_template('coordinator/members/member_modal/enrollment_form.html', view_member=view_member, states=getStates())

'''
Return the template for the demographic data in the add member modal
'''
@app.route('/coordinator/members/demographic_data', methods=['POST'])
def coordinator_members_demographic_data():
    if not session.get('login'):
        return redirect('login')
    view_member = session.get('new_member')['demographic_data']
    return render_template('coordinator/members/member_modal/demographic_data.html', view_member=view_member)

'''
Return the template for the demographic data in the add member modal in edit mode
'''
@app.route('/coordinator/members/edit/demographic_data', methods=['POST'])
def coordinator_members_edit_demographic_data():
    if not session.get('login'):
        return redirect('login')
    view_member = session.get('edit_member')['demographic_data']
    return render_template('coordinator/members/member_modal/demographic_data.html', view_member=view_member)

'''
Return the template for the self sufficiency matrix in the add member modal
'''
@app.route('/coordinator/members/self_sufficiency_matrix', methods=['POST'])
def coordinator_members_self_sufficiency_matrix():
    if not session.get('login'):
        return redirect('login')
    if session.get('modal_mode') == 'add':
        member_type = 'new_member'
    elif session.get('modal_mode') == 'edit':
        member_type = 'edit_member'
    matrix = None
    date = None
    if 'date' in request.form and request.form['date'] != "New":
        date = request.form['date']
        matrix = session.get(member_type)['self_sufficiency_matrix'][date]
    if 'key' in request.form and request.form['key'] != 'self_sufficiency_matrix' and request.form['key'] != 'self_efficacy_quiz':
        view_member = session.get(member_type)
        view_member[request.form['key']] = json.loads(request.form['data'])
        session[member_type] = view_member
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html', matrix=matrix, date=date)

'''
Return the template for the self sufficiency matrix in the add member modal in edit mode
'''
@app.route('/coordinator/members/edit/self_sufficiency_matrix', methods=['POST'])
def coordinator_members_edit_self_sufficiency_matrix():
    if not session.get('login'):
        return redirect('login')
    matrix = None
    date = None
    if 'date' in request.form and request.form['date'] != "New":
        date = request.form['date']
        matrix = session.get('edit_member')['self_sufficiency_matrix'][date]
    if 'key' in request.form and request.form['key'] != 'self_sufficiency_matrix' and request.form['key'] != 'self_efficacy_quiz':
        edit_member = session.get('edit_member')
        edit_member[request.form['key']] = json.loads(request.form['data'])
        session['edit_member'] = edit_member
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html', matrix=matrix, date=date)

'''
Save or update self sufficiency matrix values for a particular date
'''
@app.route('/coordinator/members/save_self_sufficiency_matrix', methods=['POST'])
def coordinator_members_save_self_sufficiency_matrix():
    if not session.get('login'):
        return redirect('login')
    if session.get('modal_mode') == 'add':
        member_type = 'new_member'
    elif session.get('modal_mode') == 'edit':
        member_type = 'edit_member'
    view_member = session.get(member_type)
    date = request.form['date']
    answers = json.loads(request.form['answers'])
    if date == '':
        return jsonify({"success":False, "status":400, "error_message":"date can not be blank for self sufficiency matrix"})
    if date in view_member['self_sufficiency_matrix']:
        view_member['self_sufficiency_matrix'][date] = answers
        session[member_type] = view_member
        return jsonify({"success":False, "status":400, "error_message":"Updated Self Sufficiency Matrix for " + date})
    view_member['self_sufficiency_matrix'][date] = answers
    session[member_type] = view_member
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html')

'''
Remove the self sufficiency matrix from the session
'''
@app.route('/coordinator/members/remove_self_sufficiency_matrix', methods=['POST'])
def coordinator_members_remove_self_sufficiency_matrix():
    if not session.get('login'):
        return redirect('login')
    if session.get('modal_mode') == 'add':
        member_type = 'new_member'
    elif session.get('modal_mode') == 'edit':
        member_type = 'edit_member'
    date = request.form['date']
    view_member = session.get(member_type)
    del view_member['self_sufficiency_matrix'][date]
    session[member_type] = view_member
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html')

'''
Return the template for the self efficacy quiz in the add member modal
'''
@app.route('/coordinator/members/self_efficacy_quiz', methods=['GET','POST'])
def coordinator_members_self_efficacy_quiz():
    if not session.get('login'):
        return redirect('login')
    if session.get('modal_mode') == 'add':
        member_type = 'new_member'
    elif session.get('modal_mode') == 'edit':
        member_type = 'edit_member'
    quiz = None
    date = None
    if 'date' in request.form and request.form['date'] != "New":
        date = request.form['date']
        print session.get(member_type)['self_efficacy_quiz']
        quiz = session.get(member_type)['self_efficacy_quiz'][date]
    if 'key' in request.form and request.form['key'] != 'self_efficacy_quiz' and request.form['key'] != 'self_sufficiency_matrix':
        new_member = session.get(member_type)
        new_member[request.form['key']] = json.loads(request.form['data'])
        session[member_type] = new_member
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html', quiz=quiz, date=date)

'''
Return the template for the self efficacy quiz in the add member modal
'''
@app.route('/coordinator/members/edit/self_efficacy_quiz', methods=['GET','POST'])
def coordinator_members_edit_self_efficacy_quiz():
    if not session.get('login'):
        return redirect('login')
    quiz = None
    date = None
    if 'date' in request.form and request.form['date'] != "New":
        date = request.form['date']
        print session.get('edit_member')['self_efficacy_quiz']
        quiz = session.get('edit_member')['self_efficacy_quiz'][date]
    if 'key' in request.form and request.form['key'] != 'self_efficacy_quiz' and request.form['key'] != 'self_sufficiency_matrix':
        new_member = session.get('edit_member')
        new_member[request.form['key']] = json.loads(request.form['data'])
        session['edit_member'] = new_member
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html', quiz=quiz, date=date)

'''
Save or update self efficacy quiz values for a particular date
'''
@app.route('/coordinator/members/save_self_efficacy_quiz', methods=['POST'])
def coordinator_members_save_self_efficacy_quiz():
    if not session.get('login'):
        return redirect('login')
    if session.get('modal_mode') == 'add':
        member_type = 'new_member'
    elif session.get('modal_mode') == 'edit':
        member_type = 'edit_member'
    view_member = session.get(member_type)
    date = request.form['date']
    answers = json.loads(request.form['answers'])
    if date == '':
        return jsonify({"success":False, "status":400, "error_message":"date can not be blank for self efficacy quiz"})
    if date in view_member['self_efficacy_quiz']:
        view_member['self_efficacy_quiz'][date] = answers
        session[member_type] = view_member
        return jsonify({"success":False, "status":400, "error_message":"Updated Self Efficacy Quiz for " + date})
    view_member['self_efficacy_quiz'][date] = answers
    session[member_type] = view_member
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html')

'''
Remove the self efficacy quiz from the session
'''
@app.route('/coordinator/members/remove_self_efficacy_quiz', methods=['POST'])
def coordinator_members_remove_self_efficacy_quiz():
    if not session.get('login'):
        return redirect('login')
    if session.get('modal_mode') == 'add':
        member_type = 'new_member'
    elif session.get('modal_mode') == 'edit':
        member_type = 'edit_member'
    date = request.form['date']
    view_member = session.get(member_type)
    del view_member['self_efficacy_quiz'][date]
    session[member_type] = view_member
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html')

'''
Return the template for goals in the add member modal
'''
@app.route('/coordinator/members/goals', methods=['POST'])
def coordinator_members_goals():
    if not session.get('login'):
        return redirect('login')
    return render_template('coordinator/members/member_modal/goals.html', coordinator = getCoordinator(session.get('coordinator')))

'''
Create a new member. Take the new member stored in the session,
validate that all required information is filled out, and upload the profile
picture (if it's not default). Then clear the new member object in the session.
'''
@app.route('/coordinator/members/create_member', methods=['POST'])
def coordinator_create_member():
    if not session.get('login'):
        return redirect('login')
    new_data = json.loads(request.form['new_data'])
    new_member = session.get('new_member')
    new_member[request.form['current_page']] = new_data
    
    #TODO: complete validateMember function in 'utils.py'
    validatedMember = validateMember(new_member, False)

    if validatedMember["success"]:
        profile_pic = None
        if 'profile_picture' in request.files:
            profile_pic_file = request.files['profile_picture']
            profile_pic = session.get('new_member')['general']['username'] + '.jpg'
            profile_pic_file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
        if 'profile_picture' in request.form:
            profile_pic = request.form['profile_picture']
        # profile_pic_type = request.form['profile_pic_type']

        new_member['general']['profile_picture'] = profile_pic
        session['new_member'] = new_member

        #TODO: *DATABASE* add member to database- see addMember function in db_accessor.py
        addMember(session.get('new_member'))

        session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
        return jsonify({"success":True, "status":200, "template":render_template('coordinator/members/member_modal/general.html')})
    return jsonify({"success":False, "status":400, "error_type":"validation","error_message":validatedMember["error"], "form":validatedMember["form"]})

'''
Update the member in the database. Take the updated member stored in the session,
validate that all required information is filled out, and upload the profile
picture (if it's not the same as before). Then clear the edit member object in the session.
'''
@app.route('/coordinator/members/update_member', methods=['POST'])
def coordinator_update_member():
    if not session.get('login'):
        return redirect('login')
    new_data = json.loads(request.form['new_data'])
    edit_member = session.get('edit_member')
    edit_member[request.form['current_page']] = new_data
    
    #TODO: complete validateMember function in 'utils.py'
    validatedMember = validateMember(edit_member, True)

    if validatedMember["success"]:
        profile_pic = None
        if 'profile_picture' in request.files:
            profile_pic_file = request.files['profile_picture']
            profile_pic = session.get('edit_member')['general']['username'] + '.jpg'
            profile_pic_file.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic))
            edit_member['general']['profile_picture'] = profile_pic

        session['edit_member'] = edit_member

        #TODO: *DATABASE* edit member in database- see editMember function in db_accessor.py

        editMember(session.get('edit_member'), session.get('old_edit_member'))
        session['edit_member'] = None
        session['old_edit_member'] = None
        session['modal_mode'] = 'add'
        return jsonify({"success":True, "status":200, "template":render_template('coordinator/members/add_member.html')})
    return jsonify({"success":False, "status":400, "error_type":"validation","error_message":validatedMember["error"], "form":validatedMember["form"]})

'''
Clear the new member object in the session when the new member modal is closed
'''
@app.route('/coordinator/members/clear_new_member', methods=['POST'])
def coordinator_clear_new_member():
    if not session.get('login'):
        return redirect('login')
    session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
    return render_template('coordinator/members/member_modal/general.html')

'''
Clear the member being edited from the flask session
'''
@app.route('/coordinator/members/clear_edit_member', methods=['POST'])
def coordinator_clear_edit_member():
    if not session.get('login'):
        return redirect('login')
    print "clearing edit member..."
    session['edit_member'] = None
    session['old_edit_member'] = None
    session['modal_mode'] = 'add'
    return render_template('coordinator/members/add_member.html')

# -- clubs --

'''
Coordinator clubs page
'''
@app.route('/coordinator/clubs')
def coordinator_clubs():
    if not session.get('login'):
        return redirect('login')
    return render_template('coordinator/clubs.html', coordinator = getCoordinator(session.get('coordinator')))

# -- messages --

'''
Coordinator messages page
'''
@app.route('/coordinator/messages')
def coordinator_messages():
    if not session.get('login'):
        return redirect('login')
    return render_template('coordinator/messages.html', coordinator = getCoordinator(session.get('coordinator')))

# -- other --

'''
Return the json for the google map styles
'''
@app.route('/mapstyles')
def mapstyles():
    if not session.get('login'):
        return jsonify({"status_code":400, "message":"Forbidden", "success":False})
    data = ""
    with app.open_resource("static/js/json/styles.json", "r") as data_file:
        for line in data_file:
            data += line.strip()
    return jsonify(data = data)

