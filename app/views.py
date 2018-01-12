from app import app
from flask import render_template, redirect, session, request

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

@app.route('/coordinator/home')
def coordinator_home():
    return render_template('coordinator/home.html')