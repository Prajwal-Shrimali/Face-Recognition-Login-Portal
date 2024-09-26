import mysql.connector as mysql

# CREATE DATABASE IF NOT EXISTS AWSProject;
# USE AWSProject;

# CREATE TABLE IF NOT EXISTS USERLOGIN_CREDENTIALS (
#     USER_ID INT AUTO_INCREMENT PRIMARY KEY,
#     FIRST_NAME VARCHAR(50) NOT NULL,
#     LAST_NAME VARCHAR(50) NOT NULL,
#     USERNAME VARCHAR(100) NOT NULL UNIQUE,
#     IAM_USERNAME VARCHAR(100) NOT NULL UNIQUE,
#     IAM_PASSWORD VARCHAR(255) NOT NULL,
#     APPLICATION_ACCESS_TOKEN VARCHAR(255) NOT NULL UNIQUE,
#     APPLICATION_SECRET_ACCESS_TOKEN VARCHAR(255) NOT NULL UNIQUE
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
        query = "SELECT FIRST_NAME, LAST_NAME, IAM_USERNAME, APPLICATION_ACCESS_TOKEN, APPLICATION_SECRET_ACCESS_TOKEN FROM USERLOGIN_CREDENTIALS WHERE USERNAME = %s"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        cursor.close()
        db.close()
        return row
        
    except mysql.Error as err:
        print(f"Error: {err}")
        return None