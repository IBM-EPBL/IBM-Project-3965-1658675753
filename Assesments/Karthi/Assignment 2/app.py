from flask import Flask,render_template,request,redirect,url_for

import ibm_db

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=wmx93883;PWD=uQM2V5K7w8G0j4IK;", "", "")
    print("Connected to database")
except:
    print("Failed to connect: ", ibm_db.conn_errormsg())

app = Flask(__name__)

loggedIn = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            sql = "SELECT * from user where username='{0}' and password='{1}'".format(username,password)
            print(sql)
            stmt = ibm_db.exec_immediate(conn, sql)
            res = ibm_db.fetch_assoc(stmt)
            print(res['USERNAME'])

            if len(res) == 0 :
                return render_template('login.html',message="Incorrect Username/Password")
            else:
                loggedIn = True
                return render_template('dashboard.html',user=res['USERNAME'])

        except:
            print("Error: ",ibm_db.stmt_errormsg())

    return render_template('login.html',message="")

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        rollno = request.form['rollno']
        password = request.form['password']
        cp = request.form['confirmpassword']

        if password!=cp:
            return render_template('register.html')

        try:
            sql = "INSERT into User values ('{}', '{}','{}', '{}')".format( name, email,rollno, password)
            stmt = ibm_db.exec_immediate(conn,sql)
            print("No of Affected rows: ",ibm_db.num_rows(stmt))
        except:
            print("Error: ",ibm_db.stmt_errormsg())
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if loggedIn==False:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)