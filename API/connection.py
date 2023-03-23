# Import libaries.
import mysql.connector

# Own files
import secret as s


class Connection:
    # Set cursor to None.
    sqlCursor = None

    # Initial method - Create database connection.
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="MadLibs"
        )

        self.sqlCursor = self.mydb.cursor(buffered=True)

    # Execute statement.
    def execute(self, tuple, single=False, args={}, commit=False):
        self.sqlCursor.execute(tuple, args)

        if commit == True:
            self.mydb.commit()
        else:
            if single == True:
                return self.sqlCursor.fetchone()
            else:
                return self.sqlCursor.fetchall()

    # Close connection.
    def close(self):
        mydb.close()
    
    # --------------------------- PREPERED STATEMENTS ---------------------------- #
    # ---------------------------------- CREATE ---------------------------------- #

    # ----------------------------------- READ ----------------------------------- #
    # Get user info, for login.
    def login(self, username):
        sql = f"""SELECT loginID, username, password 
                  FROM Login
                  WHERE username = '{username}'"""
        return self.execute(sql, single=True)

    
    # ---------------------------------- UPDATE ---------------------------------- #
    
    # ---------------------------------- DELETE ---------------------------------- #
    