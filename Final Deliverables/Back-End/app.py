from flask import Flask, render_template, session, request, redirect
from controllers.register import register
from controllers.login import loginUser

app = Flask(__name__)

app.secret_key = 'abc'

@app.route('/')
def homeRoute():
    if 'userId' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/login')    


@app.route('/login', methods = ['GET', 'POST'])
def loginRoute():
    if 'userId' in session:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            data = request.form
            try:
                res = loginUser(data)
                if res != -1:
                    return redirect('/')
                else:
                    return render_template('login.html')    
            except:
                return render_template('login.html')            



@app.route('/register', methods = ['GET', 'POST'])
def registerRoute():
    if 'userId' in session:
        return redirect('/')
    else:
        if request.method == 'GET':
            return render_template('register.html')
        else:
            data = request.form
            try:
                register(data)
                return redirect('/login')
            except:
                return render_template('register.html')        

@app.route('/logout')
def logoutRoute():
    session.pop('userId', None)
    return redirect('/login')  

@app.route('/profile')
def profileRoute():
    return render_template('profile.html')    