from connection import conn
import ibm_db
from flask import session
from sendgrid import Mail, SendGridAPIClient

def loginUser(data):
    email = data['email']
    password = data['password']
    response = -1

    sql = "SELECT id FROM user WHERE email = ? AND password = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    tuple = ibm_db.fetch_tuple(stmt)
    if tuple != False:
        response = tuple[0]
        session['userId'] = response
        message = Mail(
            from_email='19bcs047@mcet.in',
            to_emails='karthikseshadri7@gmail.com',
            subject='A Test from SendGrid!',
            html_content='New Jobs based on your skillset.'
        )
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
                # print(str(response.status_code))

    return response    