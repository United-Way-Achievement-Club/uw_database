from app import app
from flask import render_template, redirect, session

@app.route('/')
def index():
    if not session.get('login'):
        return redirect('login')
    else:
        member_type = session.get('member_type')
        if member_type == 'coord':
            return render_template('coordinator/home.html')
        else:
            return render_template('member/home.html')

@app.route('/login')
def login():
    return render_template('login.html')