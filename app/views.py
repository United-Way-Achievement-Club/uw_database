from app import app
from flask import render_template, redirect, session

@app.route('/')
def index():
    if not session.get('login'):
        return redirect('login')
    else:
        member_type = session.get('member_type')
        if member_type == 'coord':
            return redirect('coordinator_home')
        else:
            return redirect('member_home')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

# ==================================================  MEMBER   =====================================================

@app.route('/member')
def member():
    if not session.get('login'):
        return redirect('login')
    else:
        return redirect('member_home')

@app.route('/member/home')
def member_home():
    return render_template('member/home.html')

# ================================================= COORDINATOR ====================================================

@app.route('/coordinator')
def coordinator():
    if not session.get('login'):
        return redirect('login')
    else:
        return redirect('coordinator_home')

@app.route('/coordinator/home')
def coordinator_home():
    return render_template('coordinator/home.html')