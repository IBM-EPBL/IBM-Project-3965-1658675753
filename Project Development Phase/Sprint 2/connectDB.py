import ibm_db

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=wmx93883;PWD=uQM2V5K7w8G0j4IK;", "", "")
    print("Connected to database")
    
except:
    print("Failed to connect: ", ibm_db.conn_errormsg())