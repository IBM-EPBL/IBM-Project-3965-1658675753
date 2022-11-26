from connection import conn
import ibm_db

def register(data):
    name = data['name']
    email = data['email']
    phone = data['phno']
    password = data['password']
    sql = 'INSERT INTO user (name, email, mobile, password) values(?, ?, ?, ?)'
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, email)
    ibm_db.bind_param(stmt, 3, phone)
    ibm_db.bind_param(stmt, 4, password)
    ibm_db.execute(stmt)
