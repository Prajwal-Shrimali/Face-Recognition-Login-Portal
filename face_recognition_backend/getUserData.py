import mysql.connector as mysql

# CREATE DATABASE IF NOT EXISTS AWSProject;
# USE AWSProject;

# CREATE TABLE IF NOT EXISTS USERLOGIN_CREDENTIALS (
#     USER_ID INT AUTO_INCREMENT PRIMARY KEY,
#     FIRST_NAME VARCHAR(50) NOT NULL,
#     LAST_NAME VARCHAR(50) NOT NULL,
#     USERNAME VARCHAR(100) NOT NULL UNIQUE,
#     IAM_USERNAME VARCHAR(100) NOT NULL UNIQUE,
#     IAM_PASSWORD VARCHAR(255) NOT NULL
# );

def getUserCredentials(username):
    try:
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd="Prajwal2608$",
            database="AWSProject"
        )
        cursor = db.cursor()
        query = "SELECT IAM_USERNAME, IAM_PASSWORD FROM USERLOGIN_CREDENTIALS WHERE USERNAME = %s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        cursor.close()
        db.close()
        return row
        
    except mysql.Error as err:
        print(f"Error: {err}")
        return None