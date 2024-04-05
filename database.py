import mysql.connector

class Database:
    db_config = {
        "host":"localhost",
        "username":"root",
        "password":"root",
        "database":"stock_2"
    }

    # Connect to MySQL database
    db_connection = mysql.connector.connect(**db_config)

    #Create a cursor to execute SQL queries
    db_cursor = db_connection.cursor()
