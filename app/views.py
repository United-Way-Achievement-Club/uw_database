from app import app, db, models
from flask import render_template, redirect, session, request, jsonify, url_for
from sqlalchemy import exc
import json

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

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'user' and password == 'pass':
            session['login'] = True
            session['member_type'] = 'coord'
            member_type = 'coord'
            if member_type == 'coord':
                return redirect('coordinator/home')
            else:
                return redirect('member/home')
    return render_template('login.html', error=False)

@app.route('/logout')
def logout():
    session['login'] = False
    session['member_type'] = None
    return redirect('login')

# ==================================================  MEMBER   =====================================================

@app.route('/member')
def member():
    if not session.get('login'):
        return redirect('login')
    else:
        return redirect('member/home')

@app.route('/member/home')
def member_home():
    return render_template('member/home.html')

# ================================================= COORDINATOR ====================================================

@app.route('/coordinator')
def coordinator():
    if not session.get('login'):
        return redirect('login')
    else:
        return redirect('coordinator/home')

# -- home --

@app.route('/coordinator/home')
def coordinator_home():
    return render_template('coordinator/home.html')

# -- members --

@app.route('/coordinator/members')
def coordinator_members():
    if not session.get('new_member'):
        session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
    members = [{"image":"default_profile_pic.png", "member_name":"Example Member", "club_name":"Example Club", "goals_completed":5, "goals_in_progress":12},{"image":"sruti.png", "member_name":"Sruti B. Guhathakurta", "club_name":"Example Club", "goals_completed":10, "goals_in_progress":2}]
    return render_template('coordinator/members.html', members=members)

@app.route('/coordinator/members/update', methods=['POST'])
def coordinator_members_update():
    new_member = session.get('new_member')
    key = request.form['key']
    data = request.form['data']
    new_member[key] = json.loads(data)
    session['new_member'] = new_member
    print session.get('new_member')
    next_page = request.form['next_page']
    URL = 'coordinator_members_%s'%(next_page)
    return redirect(url_for(URL))

@app.route('/coordinator/members/general', methods=['GET','POST'])
def coordinator_members_general():
    view_member = session.get('new_member')['general']
    print view_member
    return render_template('coordinator/members/member_modal/general.html', view_member=view_member)

@app.route('/coordinator/members/enrollment_form', methods=['GET','POST'])
def coordinator_members_enrollment_form():
    return render_template('coordinator/members/member_modal/enrollment_form.html')

@app.route('/coordinator/members/demographic_data', methods=['GET','POST'])
def coordinator_members_demographic_data():
    return render_template('coordinator/members/member_modal/demographic_data.html')

@app.route('/coordinator/members/self_sufficiency_matrix', methods=['GET','POST'])
def coordinator_members_self_sufficiency_matrix():
    return render_template('coordinator/members/member_modal/self_sufficiency_matrix.html')

@app.route('/coordinator/members/self_efficacy_quiz', methods=['GET','POST'])
def coordinator_members_self_efficacy_quiz():
    return render_template('coordinator/members/member_modal/self_efficacy_quiz.html')

@app.route('/coordinator/members/goals', methods=['POST'])
def coordinator_members_goals():
    return render_template('coordinator/members/member_modal/goals.html')

@app.route('/coordinator/members/create_member', methods=['POST'])
def coordinator_create_member():
    profile_pic = None
    if 'profile_picture' in request.files:
        profile_pic = request.files['profile_picture']
    if 'profile_picture' in request.form:
        profile_pic = request.form['profile_picture']
    profile_pic_type = request.form['profile_pic_type']
    print profile_pic
    print "profile pic type: " + profile_pic_type
    return jsonify({"success":True, "status":200})

@app.route('/coordinator/members/clear_new_member')
def coordinator_clear_new_member():
    session['new_member'] = {'general':{}, 'enrollment_form':{}, 'demographic_data':{}, 'self_sufficiency_matrix':{}, 'self_efficacy_quiz':{}}
    return jsonify({"success":True, "status":200})


# -- other --

@app.route('/mapstyles')
def mapstyles():
    if not session.get('login'):
        return jsonify({"status_code":400, "message":"Forbidden", "success":False})
    data = ""
    with app.open_resource("static/js/json/styles.json", "r") as data_file:
        for line in data_file:
            data += line.strip()
    return jsonify(data = data)

