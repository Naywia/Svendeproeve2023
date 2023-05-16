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
                VALUES ('{employeeType}')"""
        self.execute(sql, commit=True)

    def insertUser(self, firstName, lastName, email, password, doorCode, phoneNumber, address, postal, employeeTypeID):
        """ Insert a new employee into the database. """
        sql = f"""INSERT INTO "Employee" ("firstName", "lastName", "email", "password", "doorCode", "phoneNumber", "address", "postal", "employeeTypeID")
            VALUES ('{firstName}', '{lastName}', '{email}', '{password}', {doorCode}, {phoneNumber}, '{address}', {postal}, {employeeTypeID});"""
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

    def insertArtefact(self, artefact, artefactDescription, artefactTypeID, placementID, artefactImage):
        """ Insert a new artefact into the database. """
        sql = f"""INSERT INTO "Artefact" ("artefact", "artefactDescription", "artefactTypeID", "placementID" """

        if artefactImage:
            sql += f""", "artefactImage") 
            VALUES ('{artefact}', '{artefactDescription}', {artefactTypeID}, {placementID}, {artefactImage});"""
        else:
            sql += f""") VALUES ('{artefact}', '{artefactDescription}', {artefactTypeID}, {placementID});"""
        self.execute(sql, commit=True)

    def insertController(self, controller, storageID):
        """ Insert a controller into the database. """
        sql = f"""INSERT INTO "Controller" ("controller", "storageID")
                VALUES ('{controller}', '{storageID}')"""
        self.execute(sql, commit=True)

    def insertLogType(self, logType):
        """ Insert a log type into the database. """
        sql = f"""INSERT INTO "LogType" ("logType")
                VALUES ('{logType}')"""
        self.execute(sql, commit=True)

    def insertLog(self, incident, incidentDate, logTypeID, controllerID):
        """ Insert a log incident into the database. """
        sql = f"""INSERT INTO "Log" ("incident", "incidentDate", "logTypeID", "controllerID")
                VALUES ('{incident}', '{incidentDate}', {logTypeID}, {controllerID})"""
        self.execute(sql, commit=True)

    # ----------------------------------- READ ----------------------------------- #
    # Get user info, for login.
    def login(self, email):
        """ Get user infomation, to login. """
        sql = f"""SELECT "employeeID", "email", "password", "employeeTypeID" 
                  FROM "Employee"
                  WHERE "email" = '{email}'"""
        return self.execute(sql, single=True)

    def unlockDoor(self, doorCode):
        """ Get door Codes. """
        sql = f"""SELECT COUNT(*)
                FROM "Employee"
                WHERE "doorCode" = '{doorCode}'"""
        result = self.execute(sql, single=True)
        if result[0] > 0:
            return "Unlocked"
        else:
            return "Couldn't unlock"

    def getPassword(self, employeeID):
        """ Get user infomation, to login. """
        sql = f"""SELECT "password"
                  FROM "Employee"
                  WHERE "employeeID" = '{employeeID}'"""
        return self.execute(sql, single=True)

    def getEmployeeTypes(self, employeeTypeID = None):
        """ Get all or one employee type. """
        sql = f"""SELECT "employeeTypeID", "employeeType"
                  FROM "EmployeeType" """
        if employeeTypeID:
            sql += f"""WHERE "employeeTypeID" = {employeeTypeID}"""    
        sql += f"""ORDER BY "employeeTypeID" ASC"""                  
        return self.execute(sql)

    def getUsers(self, employeeID = None):
        """ Get all or one user"""
        sql = f"""SELECT "employeeID", "firstName", "lastName", "email", "phoneNumber", "address", "Postal"."postal", "city", "employeeType" 
                  FROM "Employee"
                  INNER JOIN "EmployeeType" ON "Employee"."employeeTypeID" = "EmployeeType"."employeeTypeID"
                  INNER JOIN "Postal" ON "Employee"."postal" = "Postal"."postal" """
        if employeeID:
            sql += f"""WHERE "employeeID" = '{employeeID}'"""
        sql += f"""ORDER BY "employeeID" ASC"""
        return self.execute(sql)

    def getPostal(self, postal = None):
        """ Get all or one postal"""
        sql = f"""SELECT "postal", "city"
                FROM "Postal" """
        if postal:
            sql += f"""WHERE "postal" = '{postal}'"""
        sql += f"""ORDER BY "postal" ASC"""
        return self.execute(sql)

    def getStorages(self, storageID = None):
        """ Get all or one storage. """
        sql = f"""SELECT "storageID", "storageName" 
                  FROM "Storage" """
        if storageID:
            sql += f"""WHERE "storageID" = {storageID}"""
        sql += f"""ORDER BY "storageID" ASC"""
        return self.execute(sql)

    def getPlacements(self, placementID = None):
        """ Get all or one placement. """
        sql = f"""SELECT "placementID", "storageName", "shelf", "row"
                  FROM "StoragePlacement"
                  INNER JOIN "Storage" ON "StoragePlacement"."storageID" = "Storage"."storageID" """
        if placementID:
            sql += f"""WHERE "placementID" = {placementID}"""   
        sql += f"""ORDER BY "placementID" ASC"""     
        return self.execute(sql)

    def getArtefactTypes(self, artefactTypeID = None):
        """ Get all or one artefactType. """
        sql = f"""SELECT "artefactTypeID", "artefactType"
                  FROM "ArtefactType" """
        if artefactTypeID:
            sql += f"""WHERE "artefactTypeID" = {artefactTypeID}"""    
        sql += f"""ORDER BY "artefactTypeID" ASC"""                  
        return self.execute(sql)

    def getArtefacts(self, artefactID = None):
        """ Get all or one artefact. """
        sql = f"""SELECT "artefactID", "artefact", "artefactDescription", "artefactType", "storageName", "shelf", "row", "Artefact"."placementID", "artefactImage"
                  FROM "Artefact"
                  INNER JOIN "ArtefactType" ON "Artefact"."artefactTypeID" = "ArtefactType"."artefactTypeID"
                  INNER JOIN "StoragePlacement" ON "Artefact"."placementID" = "StoragePlacement"."placementID"
                  INNER JOIN "Storage" ON "StoragePlacement"."storageID" = "Storage"."storageID" """
        if artefactID:
            sql += f"""WHERE "artefactID" = {artefactID}"""    
        sql += f"""ORDER BY "artefactID" ASC"""                 
        return self.execute(sql)

    def getControllers(self, controllerID = None):
        """ Get all or one Controller. """
        sql = f"""SELECT "controllerID", "controller", "storageName"
                  FROM "Controller"
                  INNER JOIN "Storage" ON "Controller"."storageID" = "Storage"."storageID" """
        if controllerID:
            sql += f"""WHERE "controllerID" = {controllerID}"""    
        sql += f"""ORDER BY "controllerID" ASC"""                 
        return self.execute(sql)

    def getLogTypes(self, logTypeID = None):
        """ Get all or one log type. """
        sql = f"""SELECT "logTypeID", "logType"
                  FROM "LogType" """
        if logTypeID:
            sql += f"""WHERE "logTypeID" = {logTypeID}"""    
        sql += f"""ORDER BY "logTypeID" ASC"""                  
        return self.execute(sql)

    def getLogs(self, logID = None):
        """ Get all or one log incident. """
        sql = f"""SELECT "logID", "incident", "incidentDate", "logType", "controller"
                  FROM "Log"
                  INNER JOIN "LogType" ON "Log"."logTypeID" = "LogType"."logTypeID"
                  INNER JOIN "Controller" ON "Log"."controllerID" = "Controller"."controllerID" """
        if logID:
            sql += f"""WHERE "logID" = {logID}"""    
        sql += f"""ORDER BY "logID" ASC"""                 
        return self.execute(sql)

    # ---------------------------------- UPDATE ---------------------------------- #
    
    def updateUser(self, employeeID, columsToUpdate: list, values: list):
        """ Update user infomation. """

        if (len(columsToUpdate) == len(values)) and len(values) != 0:
            sql = f"""UPDATE "Employee" SET """
            i = 0
            while i < len(columsToUpdate):
                if type(values[i]) != int:
                    values[i] = "'" + values[i] + "'"
                if i == len(columsToUpdate) - 1:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]} "
                else:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]}, "
                i += 1
            sql += f"""WHERE "employeeID" = {employeeID}"""
            self.execute(sql, commit=True)
            return "User has been updated"
        return "Something went wrong"

    def updatePassword(self, employeeID, oldPassword, newPassword):
        """ Update password. """
        sql = f"""UPDATE "Employee"
                SET "password" = '{newPassword}'
                WHERE "employeeID" = {employeeID} AND "password" = '{oldPassword}';"""
        self.execute(sql, commit=True)
        return "Password has been updated"

    def updateEmployeeType(self, employeeTypeID, employeeType):
        """ Update employee type. """
        sql = f"""UPDATE "EmployeeType"
                SET "employeeType" = '{employeeType}'
                WHERE "employeeTypeID" = {employeeTypeID};"""
        self.execute(sql, commit=True)
        return "Employee type has been updated"

    def updateStorage(self, storageID, storageName):
        """ Update storage. """
        sql = f"""UPDATE "Storage"
                SET "storageName" = '{storageName}'
                WHERE "storageID" = {storageID};"""
        self.execute(sql, commit=True)
        return "Storage has been updated"

    def updatePlacement(self, placementID, columsToUpdate: list, values: list):
        """ Update storage placement. """

        if (len(columsToUpdate) == len(values)) and len(values) != 0:
            sql = f"""UPDATE "StoragePlacement" SET """
            i = 0
            while i < len(columsToUpdate):
                if type(values[i]) != int:
                    values[i] = "'" + values[i] + "'"
                if i == len(columsToUpdate) - 1:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]} "
                else:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]}, "
                i += 1
            sql += f"""WHERE "placementID" = {placementID}"""
            self.execute(sql, commit=True)
            return "Placement has been updated"
        return "Something went wrong"
    
    def updateArtefactType(self, artefactTypeID, artefactType):
        """ Update artefact type. """
        sql = f"""UPDATE "ArtefactType"
                SET "artefactType" = '{artefactType}'
                WHERE "artefactTypeID" = {artefactTypeID};"""
        self.execute(sql, commit=True)
        return "Artefact type has been updated"

    def updateArtefact(self, artefactID, columsToUpdate: list, values: list):
        """ Update artefact. """

        if (len(columsToUpdate) == len(values)) and len(values) != 0:
            sql = f"""UPDATE "Artefact" SET """
            i = 0
            while i < len(columsToUpdate):
                if type(values[i]) != int:
                    values[i] = "'" + values[i] + "'"
                if i == len(columsToUpdate) - 1:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]} "
                else:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]}, "
                i += 1
            sql += f"""WHERE "artefactID" = {artefactID}"""
            self.execute(sql, commit=True)
            return "Artefact has been updated"
        return "Something went wrong"

    def updateController(self, controllerID, columsToUpdate: list, values: list):
        """ Update controller. """

        if (len(columsToUpdate) == len(values)) and len(values) != 0:
            sql = f"""UPDATE "Controller" SET """
            i = 0
            while i < len(columsToUpdate):
                if type(values[i]) != int:
                    values[i] = "'" + values[i] + "'"
                if i == len(columsToUpdate) - 1:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]} "
                else:
                    sql += f"\"{columsToUpdate[i]}\" = {values[i]}, "
                i += 1
            sql += f"""WHERE "controllerID" = {controllerID}"""
            self.execute(sql, commit=True)
            return "Controller has been updated"
        return "Something went wrong"

    def updateLogType(self, logTypeID, logType):
        """ Update log type. """
        sql = f"""UPDATE "LogType"
                SET "logType" = '{logType}'
                WHERE "logTypeID" = {logTypeID};"""
        self.execute(sql, commit=True)
        return "Artefact type has been updated"

    # ---------------------------------- DELETE ---------------------------------- #
    
    def deleteEmployeeType(self, employeeTypeID):
        """ Delete employee type. """
        sql = f"""DELETE FROM "EmployeeType"
                WHERE "employeeTypeID" = '{employeeTypeID}'"""
        return self.execute(sql, commit=True)

    def deleteUser(self, employeeID, what="employeeID"):
        """ Delete user"""
        sql = f"""DELETE FROM "Employee"
                WHERE "employeeID" = '{employeeID}'"""
        return self.execute(sql, commit=True)

    def deleteStorage(self, storageID):
        """ Delete storage. """
        self.deletePlacement(storageID, what="storageID")
        sql = f"""DELETE FROM "Storage"
                WHERE "storageID" = {storageID}"""
        return self.execute(sql, commit=True)

    def deletePlacement(self, ID, what = "placementID"):
        """ Delete placement. """
        if what == "placementID":
            self.deleteArtefact(ID, what=what)
        else:
            delete = f"""SELECT "placementID" FROM "StoragePlacement" WHERE "{what}" = {ID}"""
            ids = self.execute(delete)
            for id in ids:
                self.deleteArtefact(id, what="placementID")
        sql = f"""DELETE FROM "StoragePlacement"
                WHERE "{what}" = {ID}"""        
        return self.execute(sql, commit=True)

    def deleteArtefactType(self, artefactTypeID):
        """ Delete artefactType. """
        self.deleteArtefact(artefactTypeID, what="artefactTypeID")
        sql = f"""DELETE FROM "ArtefactType"
                WHERE "artefactTypeID" = {artefactTypeID}"""                
        return self.execute(sql, commit=True)

    def deleteArtefact(self, ID, what = "artefactID"):
        """ Delete artefact. """
        sql = f"""DELETE FROM "Artefact"
                WHERE "{what}" = {ID}"""         
        return self.execute(sql, commit=True)

    def deleteController(self, controllerID):
        """ Delete controller. """
        self.deleteLog(controllerID, what="controllerID")
        sql = f"""DELETE FROM "Controller"
                WHERE "controllerID" = {controllerID}"""                
        return self.execute(sql, commit=True)

    def deleteLogType(self, logTypeID):
        """ Delete logType. """
        self.deleteLog(logTypeID, what="logTypeID")
        sql = f"""DELETE FROM "LogType"
                WHERE "logTypeID" = {logTypeID}"""                
        return self.execute(sql, commit=True)

    def deleteLog(self, ID, what = "logID"):
        """ Delete Log. """
        sql = f"""DELETE FROM "Log"
                WHERE "{what}" = {ID}"""         
        return self.execute(sql, commit=True)