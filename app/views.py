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

        # TODO: remove hardcoded user check and actually check for user in database

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

    #TODO: replace members list above with proper query from the database

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
    new_member[key] = json.loads(data)
    session['new_member'] = new_member
    next_page = request.form['next_page']
    URL = 'coordinator_members_%s'%(next_page)
    return redirect(url_for(URL))

'''
Return the template for the general page in the add member modal
'''
@app.route('/coordinator/members/general', methods=['GET','POST'])
def coordinator_members_general():
    view_member = session.get('new_member')['general']
    return render_template('coordinator/members/member_modal/general.html', view_member=view_member)

'''
Return the template for the enrollment form in the add member modal
'''
@app.route('/coordinator/members/enrollment_form', methods=['GET','POST'])
def coordinator_members_enrollment_form():
    view_member = session.get('new_member')['enrollment_form']
    print view_member
    return render_template('coordinator/members/member_modal/enrollment_form.html', view_member=view_member)

'''
Return the template for the demographic data in the add member modal
'''
@app.route('/coordinator/members/demographic_data', methods=['GET','POST'])
def coordinator_members_demographic_data():
    #TODO: pass the member information from the session into the template
    return render_template('coordinator/members/member_modal/demographic_data.html')

'''
Return the template for the self sufficiency matrix in the add member modal
'''
@app.route('/coordinator/members/self_sufficiency_matrix', methods=['GET','POST'])
def coordinator_members_self_sufficiency_matrix():
    #TODO: pass the member information from the session into the template
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html')

'''
Return the template for the self efficacy quiz in the add member modal
'''
@app.route('/coordinator/members/self_efficacy_quiz', methods=['GET','POST'])
def coordinator_members_self_efficacy_quiz():
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
    #TODO: validate fields in the new member object
    profile_pic = None
    if 'profile_picture' in request.files:
        profile_pic = request.files['profile_picture']
    if 'profile_picture' in request.form:
        profile_pic = request.form['profile_picture']
    profile_pic_type = request.form['profile_pic_type']
    print profile_pic
    print "profile pic type: " + profile_pic_type

    #TODO: add member to database

    session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
    return jsonify({"success":True, "status":200})

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

