from flask import Flask , render_template , request, session
import ibm_db
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
 
app = Flask(__name__)

app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt;UID=wmx93883;PWD=uQM2V5K7w8G0j4IK",'','')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg="  "
       
    
    if request.method == 'POST' :
        name = request.form['name']
        password = request.form['password']
        sql = "SELECT * FROM USER WHERE name =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['NAME']
            userid=  account['NAME']
            session['name'] = account['NAME']
            msg = 'Logged in successfully !'
            message = Mail(
            from_email='19bcs047@mcet.in',
            to_emails='19bcs055@mcet.in',
            subject='A Test from SendGrid!',
            html_content='<strong>Hello there from SendGrid your URL is: ' +
            '<a href=''https://github.com/cyberjive''>right here!</a></strong>')
            try:
                sg = SendGridAPIClient('SENDGRID_API_KEY')
                response = sg.send(message)
                code, body, headers = response.status_code, response.body, response.headers
                print(f"Response Code: {code} ")
                print(f"Response Body: {body} ")
                print(f"Response Headers: {headers} ")
                print("Message Sent!")
            except Exception as e:
                print("Error: {0}".format(e))
                print(str(response.status_code))
        return render_template('dashboard.html', msg = msg)
    else:
            msg = 'Incorrect name / password !'
    return render_template('login.html', msg = msg)

@app.route('/', methods =['GET', 'POST'])
def register():
    msg =" "
    if request.method == 'POST' :
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        rollno = request.form['rollno']
        sql = "SELECT * FROM USER WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  USER VALUES (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, rollno)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html',msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/profile')
def renderProfile():
    return render_template('profile.html')    
    
if __name__ == '__main__':
   app.run()