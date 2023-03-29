# Import libaries.
import psycopg2

# Own files

class Connection:
    # Set cursor to None.
    sqlCursor = None
    conn = None

    # Initial method - Create database connection.
    def __init__(self):
        #Connect to the PostgreSQL database server.
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="archaeologygallery",
                user="GoatMaster",
                password="P@ssw0rd!"
                )
            
            # create a cursor
            self.sqlCursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # Execute statement.
    def execute(self, sql, single=False, args=(), commit=False):
        self.sqlCursor.execute(sql, args)

        if commit == True:
            self.conn.commit()
        else:
            if single == True:
                return self.sqlCursor.fetchone()
            else:
                return self.sqlCursor.fetchall()

    # Close connection.
    def close(self):
        self.conn.close()
    
    # --------------------------- PREPERED STATEMENTS ---------------------------- #
    # ---------------------------------- CREATE ---------------------------------- #
    def insertEmployeeType(self, employeeType):
        """ Insert a employee type into the database. """
        sql = f"""INSERT INTO "EmployeeType" ("employeeType")
            VALUES ('{employeeType}');"""
        self.execute(sql, commit=True)

    def insertUser(self, firstName, lastName, email, password, doorCode, phoneNumber, employeeTypeID):
        """ Insert a new employee into the database. """
        sql = f"""INSERT INTO "Employee" ("firstName", "lastName", "email", "password", "doorCode", "phoneNumber", "employeeTypeID")
            VALUES ('{firstName}', '{lastName}', '{email}', '{password}', {doorCode}, {phoneNumber}, {employeeTypeID});"""
        self.execute(sql, commit=True)

    def insertStorage(self, storageName):
        """ Insert a new storage into the database. """
        sql = f"""INSERT INTO "Storage" ("storageName")
            VALUES ('{storageName}');"""
        self.execute(sql, commit=True)

    def insertPlacement(self, shelf, row, storageID):
        """ Insert a new storage placement into the database. """
        sql = f"""INSERT INTO "StoragePlacement" ("shelf", "row", "storageID")
            VALUES ('{shelf}', '{row}', {storageID});"""
        self.execute(sql, commit=True)

    def insertArtefactType(self, artefactType):
        """ Insert a new artefact type into the database. """
        sql = f"""INSERT INTO "ArtefactType" ("artefactType")
            VALUES ('{artefactType}');"""
        self.execute(sql, commit=True)

    def insertArtefact(self, artefact, artefactDescription, artefactTypeID, placementID):
        """ Insert a new artefact into the database. """
        sql = f"""INSERT INTO "Artefact" ("artefact", "artefactDescription", "artefactTypeID", "placementID")
            VALUES ('{artefact}', '{artefactDescription}', {artefactTypeID}, {placementID});"""
        self.execute(sql, commit=True)

    # ----------------------------------- READ ----------------------------------- #
    # Get user info, for login.
    def login(self, email):
        """ Get user infomation, to login. """
        sql = f"""SELECT "employeeID", "email", "password", "employeeTypeID" 
                  FROM "Employee"
                  WHERE "email" = '{email}'"""
        return self.execute(sql, single=True)

    def getUsers(self, employeeID = None):
        """ Get all or one user"""
        sql = f"""SELECT "employeeID", "firstName", "lastName", "email", "phoneNumber", "employeeType" 
                  FROM "Employee"
                  INNER JOIN "EmployeeType" ON "Employee"."employeeTypeID" = "EmployeeType"."employeeTypeID" """
        if employeeID:
            sql += f"""WHERE "employeeID" = '{employeeID}'"""
        return self.execute(sql)

    def getStorages(self, storageID = None):
        """ Get all or one storage. """
        sql = f"""SELECT "storageID", "storageName" 
                  FROM "Storage" """
        if storageID:
            sql += f"""WHERE "storageID" = {storageID}"""
        return self.execute(sql)

    def getPlacements(self, placementID = None):
        """ Get all or one placement. """
        sql = f"""SELECT "placementID", "storageName", "shelf", "row"
                  FROM "StoragePlacement"
                  INNER JOIN "Storage" ON "StoragePlacement"."storageID" = "Storage"."storageID" """
        if placementID:
            sql += f"""WHERE "placementID" = {placementID}"""        
        return self.execute(sql)

    def getArtefactTypes(self, artefactTypeID = None):
        """ Get all or one artefactType. """
        sql = f"""SELECT "artefactTypeID", "artefactType"
                  FROM "ArtefactType" """
        if artefactTypeID:
            sql += f"""WHERE "artefactTypeID" = {artefactTypeID}"""                
        return self.execute(sql)

    def getArtefacts(self, artefactID = None):
        """ Get all or one artefact. """
        sql = f"""SELECT "artefactID", "artefact", "artefactDescription", "artefactType", "storageName", "shelf", "row" 
                  FROM "Artefact"
                  INNER JOIN "ArtefactType" ON "Artefact"."artefactTypeID" = "ArtefactType"."artefactTypeID"
                  INNER JOIN "StoragePlacement" ON "Artefact"."placementID" = "StoragePlacement"."placementID"
                  INNER JOIN "Storage" ON "StoragePlacement"."storageID" = "Storage"."storageID" """
        if artefactID:
            sql += f"""WHERE "artefactID" = {artefactID}"""         
        return self.execute(sql)

    # ---------------------------------- UPDATE ---------------------------------- #
    def updateStorage(self, storageID, storageName):
        """ Update storage. """
        sql = f"""UPDATE "Storage"
                SET "storageName" = '{storageName}'
                WHERE "storageID" = {storageID};"""
        self.execute(sql, commit=True)
        return "Storage has been updated"

    def UpdatePlacement(self, placementID, columsToUpdate: list, values: list):
        """ Update storage. """

        if (len(columsToUpdate) == len(values)) and len(values) != 0:
            sql = f"""UPDATE "StoragePlacement" SET """
            i = 0
            while i < len(columsToUpdate):
                if columsToUpdate[i] != "storageID":
                    values[i] = "'" + values[i] + "'"
                if i == len(columsToUpdate) - 1:
                    sql += f"{columsToUpdate[i]} = {values[i]} "
                else:
                    sql += f"{columsToUpdate[i]} = {values[i]}, "
                i += 1
            sql += f""""WHERE "placementID" = {bookID}"""
            self.execute(sql, commit=True)
            return "Placement has been updated"
        return "Something went wrong"

        sql = f"""UPDATE table_name
                SET column1 = value1,
                column2 = value2
                WHERE condition;"""
        return self.execute(sql)

    # ---------------------------------- DELETE ---------------------------------- #
    