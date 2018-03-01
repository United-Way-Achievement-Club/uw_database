'''
Title
-----
views.py

Description
-----------
Handle requests to the server by returning proper data or template

'''
from app import app, db, models
from flask import render_template, redirect, session, request, jsonify, url_for
from sqlalchemy import exc
import json
from utils import validateMember, getStates


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
        if member_type == 'coord':
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

        # TODO: *DATABASE* remove hardcoded user check and actually check for user in database

        if username == 'user' and password == 'pass':
            session['login'] = True
            session['member_type'] = 'coord'
            member_type = 'coord'
            if member_type == 'coord':
                return redirect('coordinator/home')
            else:
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
    return render_template('member/home.html')

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
    return render_template('coordinator/home.html')

# -- goals --

'''
Coordinator goals page
'''
@app.route('/coordinator/goals')
def coordinator_goals():
    return render_template('coordinator/goals.html')

# -- approve --

'''
Coordinator approve page
'''
@app.route('/coordinator/approve')
def coordinator_approve():
    return render_template('coordinator/approve.html')

# -- members --

'''
Coordinator members page
Query members from the database and send to template
'''
@app.route('/coordinator/members')
def coordinator_members():
    if not session.get('new_member'):
        session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
    members = [{"image":"default_profile_pic.png", "member_name":"Example Member", "club_name":"Example Club", "goals_completed":5, "goals_in_progress":12},{"image":"sruti.png", "member_name":"Sruti B. Guhathakurta", "club_name":"Example Club", "goals_completed":10, "goals_in_progress":2}]

    #TODO: *DATABASE* replace members list above with proper query from the database

    return render_template('coordinator/members.html', members=members)

'''
Update the current page in the add member modal
accept a key (the old page name), data(the data from the old page)
and the next page. Store the data from the old page in the
session temporarily, then redirect to the next page.
'''
@app.route('/coordinator/members/update', methods=['POST'])
def coordinator_members_update():
    new_member = session.get('new_member')
    key = request.form['key']
    data = request.form['data']
    if key != 'self_sufficiency_matrix' and key != 'self_efficacy_quiz':
        new_member[key] = json.loads(data)
        session['new_member'] = new_member
    print session.get('new_member')
    next_page = request.form['next_page']
    URL = 'coordinator_members_%s'%(next_page)
    return redirect(url_for(URL), code=307)

'''
Return the template for the general page in the add member modal
'''
@app.route('/coordinator/members/general', methods=['POST'])
def coordinator_members_general():
    view_member = session.get('new_member')['general']
    return render_template('coordinator/members/member_modal/general.html', view_member=view_member)

'''
Return the template for the enrollment form in the add member modal
'''
@app.route('/coordinator/members/enrollment_form', methods=['POST'])
def coordinator_members_enrollment_form():
    view_member = session.get('new_member')['enrollment_form']
    return render_template('coordinator/members/member_modal/enrollment_form.html', view_member=view_member, states=getStates())

'''
Return the template for the demographic data in the add member modal
'''
@app.route('/coordinator/members/demographic_data', methods=['POST'])
def coordinator_members_demographic_data():
    view_member = session.get('new_member')['demographic_data']
    return render_template('coordinator/members/member_modal/demographic_data.html', view_member=view_member)

'''
Return the template for the self sufficiency matrix in the add member modal
'''
@app.route('/coordinator/members/self_sufficiency_matrix', methods=['POST'])
def coordinator_members_self_sufficiency_matrix():
    matrix = None
    date = None
    if 'date' in request.form and request.form['date'] != "New":
        date = request.form['date']
        matrix = session.get('new_member')['self_sufficiency_matrix'][date]
    if 'key' in request.form and request.form['key'] != 'self_sufficiency_matrix' and request.form['key'] != 'self_efficacy_quiz':
        new_member = session.get('new_member')
        new_member[request.form['key']] = json.loads(request.form['data'])
        session['new_member'] = new_member
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html', matrix=matrix, date=date)

'''
Save or update self sufficiency matrix values for a particular date
'''
@app.route('/coordinator/members/save_self_sufficiency_matrix', methods=['POST'])
def coordinator_members_save_self_sufficiency_matrix():
    view_member = session.get('new_member')
    date = request.form['date']
    answers = json.loads(request.form['answers'])
    if date == '':
        return jsonify({"success":False, "status":400, "error_message":"date can not be blank for self sufficiency matrix"})
    if date in view_member['self_sufficiency_matrix']:
        view_member['self_sufficiency_matrix'][date] = answers
        session['new_member'] = view_member
        return jsonify({"success":False, "status":400, "error_message":"Updated Self Sufficiency Matrix for " + date})
    view_member['self_sufficiency_matrix'][date] = answers
    session['new_member'] = view_member
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html')

@app.route('/coordinator/members/remove_self_sufficiency_matrix', methods=['POST'])
def coordinator_members_remove_self_sufficiency_matrix():
    date = request.form['date']
    view_member = session.get('new_member')
    del view_member['self_sufficiency_matrix'][date]
    session['new_member'] = view_member
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html')

'''
Return the template for the self efficacy quiz in the add member modal
'''
@app.route('/coordinator/members/self_efficacy_quiz', methods=['GET','POST'])
def coordinator_members_self_efficacy_quiz():
    quiz = None
    date = None
    if 'date' in request.form and request.form['date'] != "New":
        date = request.form['date']
        print session.get('new_member')['self_efficacy_quiz']
        quiz = session.get('new_member')['self_efficacy_quiz'][date]
    if 'key' in request.form and request.form['key'] != 'self_efficacy_quiz' and request.form['key'] != 'self_sufficiency_matrix':
        new_member = session.get('new_member')
        new_member[request.form['key']] = json.loads(request.form['data'])
        session['new_member'] = new_member
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html', quiz=quiz, date=date)

'''
Save or update self efficacy quiz values for a particular date
'''
@app.route('/coordinator/members/save_self_efficacy_quiz', methods=['POST'])
def coordinator_members_save_self_efficacy_quiz():
    view_member = session.get('new_member')
    date = request.form['date']
    answers = json.loads(request.form['answers'])
    if date == '':
        return jsonify({"success":False, "status":400, "error_message":"date can not be blank for self efficacy quiz"})
    if date in view_member['self_efficacy_quiz']:
        view_member['self_efficacy_quiz'][date] = answers
        session['new_member'] = view_member
        return jsonify({"success":False, "status":400, "error_message":"Updated Self Efficacy Quiz for " + date})
    view_member['self_efficacy_quiz'][date] = answers
    session['new_member'] = view_member
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html')

@app.route('/coordinator/members/remove_self_efficacy_quiz', methods=['POST'])
def coordinator_members_remove_self_efficacy_quiz():
    date = request.form['date']
    view_member = session.get('new_member')
    del view_member['self_efficacy_quiz'][date]
    session['new_member'] = view_member
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html')

'''
Return the template for goals in the add member modal
'''
@app.route('/coordinator/members/goals', methods=['POST'])
def coordinator_members_goals():
    return render_template('coordinator/members/member_modal/goals.html')

'''
Create a new member. Take the new member stored in the session,
validate that all required information is filled out, and add
the member to the database. Then clear the new member object in the session.
'''
@app.route('/coordinator/members/create_member', methods=['POST'])
def coordinator_create_member():
    new_data = json.loads(request.form['new_data'])
    new_member = session.get('new_member')
    new_member[request.form['current_page']] = new_data
    session['new_member'] = new_member

    #TODO: validate fields in the new member object- edit validateMember function in 'utils.py'

    validatedMember = validateMember(session.get('new_member'))
    if validatedMember["success"]:
        profile_pic = None
        if 'profile_picture' in request.files:
            profile_pic = request.files['profile_picture']
        if 'profile_picture' in request.form:
            profile_pic = request.form['profile_picture']
        profile_pic_type = request.form['profile_pic_type']
        print profile_pic
        print "profile pic type: " + profile_pic_type

        #TODO: upload profile picture

        #TODO: *DATABASE* add member to database

        session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
        return jsonify({"success":True, "status":200})
    return jsonify({"success":False, "status":400, "error_type":"validation","error_message":validatedMember["error"], "form":validatedMember["form"]})

'''
Clear the new member object in the session when the new member modal is closed
'''
@app.route('/coordinator/members/clear_new_member', methods=['POST'])
def coordinator_clear_new_member():
    session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
    return render_template('coordinator/members/member_modal/general.html')

# -- clubs --

'''
Coordinator clubs page
'''
@app.route('/coordinator/clubs')
def coordinator_clubs():
    return render_template('coordinator/clubs.html')

# -- messages --

'''
Coordinator messages page
'''
@app.route('/coordinator/messages')
def coordinator_messages():
    return render_template('coordinator/messages.html')

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

