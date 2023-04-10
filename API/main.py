# IMPORTS.
# Libaries / Frameworks.
import datetime
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

import paho.mqtt.client as mqtt #import the client
import json

# Own files.
from connection import Connection as Conn
from authorize import Authorize
from basemodels import *

class Mosquitto:
    def __init__(self):
        self.client = mqtt.Client() #create new instance
        self.client.username_pw_set("user", "P@ssw0rd!")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1", 1883) #connect to broker

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if the connection is lost and reconnected, then subscriptions will be renewed.
        client.subscribe("security")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")

        if "{" in payload:
            data = json.loads(payload)

            print(payload + " received on topic[" + msg.topic + "]")

            Conn().insertLog(data["incident"], data["incidentDate"], data["logTypeID"], data["controllerID"])

        else:
            print(payload)

# API
class Archaeologygallery:
    # Make variable for the api.
    api = FastAPI() 

    # Get access token.
    @api.post("/login", summary="Login")
    async def login(form_data: OAuth2PasswordRequestForm = Depends()):
        """ Login endpoint. """
        # Expire JWT after 15 minutes.
        ACCESS_TOKEN_EXPIRE_MINUTES = 15

        user = Authorize().authenticateUser(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                content={"Message": "Incorrect username or password."},
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        accessToken = Authorize().createAccessToken(data={"sub": user[1], "role": user[3]}, expires_delta=access_token_expires)

        content = {"access_token": accessToken, "token_type": "bearer","Message": "You've logged in.", "employeeID": user[0]}
        headers = {"Authorization": f"Bearer {accessToken}"}
        return JSONResponse(content=content, headers=headers)

    # -------------------------------------- CREATE -------------------------------------- #

    @api.post("/employeeType", status_code=201, summary="Create new employee type.")
    async def addEmployeeType(eType: EmployeeType, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new user. """
        Conn().insertEmployeeType(eType.employeeType)
        return {'message': 'Employee type has been created'}

    # Create a new user. 
    @api.post("/user", status_code=201, summary="Create new employee.")
    async def addUser(user: User, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new user. """
        Conn().insertUser(user.firstName, user.lastName, user.email, Authorize().hashPassword(user.password), user.doorCode, user.phoneNumber, user.address, user.postal, user.employeeTypeID)
        return {'message': 'User has been created'}

    @api.post("/storage", status_code=201, summary="Create new storage.")
    async def addStorage(storage: Storage, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new storage room. """
        Conn().insertStorage(storage.storageName)
        return {'message': 'Storage has been created'}

    @api.post("/placement", status_code=201, summary="Create new storage placement.")
    async def addPlacement(placement: StoragePlacement, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new storage placement. """
        Conn().insertPlacement(placement.shelf, placement.row, placement.storageID)
        return {'message': 'Placement has been created'}

    @api.post("/artefactType", status_code=201, summary="Create new artefact type.")
    async def addArtefactType(aType: ArtefactType, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new artefact type. """
        Conn().insertArtefactType(aType.artefactType)
        return {'message': 'artefactType has been created'}

    @api.post("/artefact", status_code=201, summary="Create new artefact.")
    async def addArtefact(artefact: Artefact, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new user. """
        Conn().insertArtefact(artefact.artefact, artefact.artefactDescription, artefact.artefactTypeID, artefact.placementID)
        return {'message': 'Artefact has been created'}

    @api.post("/logType", status_code=201, summary="Create new log type.")
    async def addLogType(lType: LogType, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new log type. """
        Conn().insertLogType(lType.logType)
        return {'message': 'Log type has been created'}

    @api.post("/controller", status_code=201, summary="Create new controller.")
    async def addController(cntr: Controller, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new log. """
        Conn().insertController(cntr.controller, cntr.storageID)
        return {'message': 'Controller has been created'}

    @api.post("/log", status_code=201, summary="Create new log incident.")
    async def addLog(log: Log, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new log. """
        Conn().insertLog(log.incident, log.incidentDate, log.logTypeID)
        return {'message': 'Log incident has been created'}

    # --------------------------------------- READ --------------------------------------- #

    @api.get("/employeeType", summary="Get all or one employee type.")
    async def getEmployeeType(employeeTypeID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new user. """
        # If the employeeTypeID isn't none.
        result = []
        if employeeTypeID:
            title = "empType"
            empTypes = Conn().getEmployeeTypes(employeeTypeID)
        else:
            title = "empType"
            empTypes = Conn().getEmployeeTypes()
        i = 0
        while i < len(empTypes):
            temp = {}
            temp['ID'] = empTypes[i][0]
            temp['EmployeeType'] = empTypes[i][1]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/user", summary="Get all or one user")
    async def getUser(userID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all users or one specific user. """
        # If the userID isn't none.
        result = []
        if userID:
            title = "User"
            users = Conn().getUsers(userID)
        else:
            title = "Users"
            users = Conn().getUsers()
        i = 0
        while i < len(users):
            temp = {}
            temp['ID'] = users[i][0]
            temp['FirstName'] = users[i][1]
            temp['LastName'] = users[i][2]
            temp['Email'] = users[i][3]
            temp['PhoneNumber'] = users[i][4]
            temp['Address'] = users[i][5]
            temp['Postal'] = users[i][6]
            temp['City'] = users[i][7]
            temp['EmployeeType'] = users[i][8]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/postal", summary="Get all or one postal")
    async def getPostal(postal: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all users or one specific user. """
        # If the postal isn't none.
        result = []
        if postal:
            title = "Postal"
            postalCity = Conn().getPostal(postal)
        else:
            title = "Postals"
            postalCity = Conn().getPostal()
        i = 0
        while i < len(postalCity):
            temp = {}
            temp['Postal'] = postalCity[i][0]
            temp['City'] = postalCity[i][1]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/storage", summary="Get all or one storage")
    async def getStorage(storageID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all storages or one specific storage. """
        # If the storageID isn't none.
        result = []
        if storageID:
            title = "Storage"
            storages = Conn().getStorages(storageID)
        else:
            title = "Storages"
            storages = Conn().getStorages()
        i = 0
        while i < len(storages):
            temp = {}
            temp['ID'] = storages[i][0]
            temp['Name'] = storages[i][1]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/placement", summary="Get all or one storage placement")
    async def getPlacement(placementID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all placements or one specific placement. """
        # If the placementID isn't none.
        result = []
        if placementID:
            title = "Placement"
            placements = Conn().getPlacements(placementID)
        else:
            title = "Placements"
            placements = Conn().getPlacements()
        i = 0
        while i < len(placements):
            temp = {}
            temp['ID'] = placements[i][0]
            temp['Storage'] = placements[i][1]
            temp['Shelf'] = placements[i][2]
            if placements[i][3]:
                temp['Row'] = placements[i][3]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/artefactType", summary="Get all or one artefact type")
    async def getArtefactType(artefactTypeID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all artefact types or one specific artefact type. """
        # If the artefactTypeID isn't none.
        result = []
        if artefactTypeID:
            title = "Artefact Type"
            atypes = Conn().getArtefactTypes(artefactTypeID)
        else:
            title = "Artefact Types"
            atypes = Conn().getArtefactTypes()
        i = 0
        while i < len(atypes):
            temp = {}
            temp['ID'] = atypes[i][0]
            temp['Type'] = atypes[i][1]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/artefact", summary="Get all or one artefact")
    async def getArtefact(artefactID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all artefacts or one specific artefact. """
        # If the artefactID isn't none.
        result = []
        if artefactID:
            title = "Artefact"
            artefacts = Conn().getArtefacts(artefactID)
        else:
            title = "Artefacts"
            artefacts = Conn().getArtefacts()
        i = 0
        while i < len(artefacts):
            temp = {}
            temp['ID'] = artefacts[i][0]
            temp['Name'] = artefacts[i][1]
            temp['Description'] = artefacts[i][2]
            temp['ArtefactType'] = artefacts[i][3]
            temp['Storage'] = artefacts[i][4]
            temp['Shelf'] = artefacts[i][5]
            if artefacts[i][6]:
                temp['Row'] = artefacts[i][6]

            result.append(temp)
            i += 1
            
        return {title: result}

    @api.get("/logType", summary="Get all or one log type.")
    async def getLogType(logTypeID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all log types or one specific log type. """
        # If the logTypeID isn't none.
        result = []
        if logTypeID:
            title = "Log Type"
            ltypes = Conn().getLogTypes(logTypeID)
        else:
            title = "Log Types"
            ltypes = Conn().getLogTypes()
        i = 0
        while i < len(ltypes):
            temp = {}
            temp['ID'] = ltypes[i][0]
            temp['Type'] = ltypes[i][1]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/controller", summary="Get all or one controller.")
    async def getController(controllerID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all controllers or one specific controller. """
        # If the controllerID isn't none.
        result = []
        if controllerID:
            title = "Controller"
            cntrs = Conn().getControllers(controllerID)
        else:
            title = "Controllers"
            cntrs = Conn().getControllers()
        i = 0
        while i < len(cntrs):
            temp = {}
            temp['ID'] = cntrs[i][0]
            temp['Controller'] = cntrs[i][1]
            temp['Storage'] = cntrs[i][2]

            result.append(temp)
            i += 1
        return {title: result}

    @api.get("/log", summary="Get all or one log indicent.")
    async def getLog(logID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for getting all log types or one specific log type. """
        # If the logID isn't none.
        result = []
        if logID:
            title = "Log_incident"
            logs = Conn().getLogs(logID)
        else:
            title = "Log_incidents"
            logs = Conn().getLogs()
        i = 0
        while i < len(logs):
            temp = {}
            temp['ID'] = logs[i][0]
            temp['Incident'] = logs[i][1]
            temp['IncidentDate'] = logs[i][2]
            temp['Type'] = logs[i][3]

            result.append(temp)
            i += 1
        return {title: result}

    # -------------------------------------- UPDATE -------------------------------------- #

    @api.patch("/employeeType", summary="Update employee type")
    async def updateEmployeeType(employeeTypeID: int, eType: EmployeeType, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating an employee type. """
        result = Conn().updateEmployeeType(employeeTypeID, eType.employeeType)
        return {'message': result}

    @api.patch("/user", summary="Update user")
    async def updateUser(userID: int, user: UpdateUser, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating user infomation. """
        columsToUpdate = []
        values = []

        # If values isn't none add them to list.
        if user.firstName:
            columsToUpdate.append("firstName")
            values.append(user.firstName)
        if user.lastName:
            columsToUpdate.append("lastName")
            values.append(user.lastName)
        if user.email:
            columsToUpdate.append("email")
            values.append(user.email)
        if user.phoneNumber:
            columsToUpdate.append("phoneNumber")
            values.append(user.phoneNumber)
        if user.address:
            columsToUpdate.append("address")
            values.append(user.address)
        if user.postal:
            columsToUpdate.append("postal")
            values.append(user.postal)
        if user.employeeTypeID:
            columsToUpdate.append("employeeTypeID")
            values.append(user.employeeTypeID)

        result = Conn().updateUser(userID, columsToUpdate, values)
        if result == "Something went wrong":
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": result}

    @api.patch("/password", summary="Update user password")
    async def updatePassword(userID: int, psw: UpdatePsw, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating a users password. """
        hashed_password = Conn().getPassword(userID)
        if Authorize().verifyPassword(oldPassword, hashed_password):
            if psw.newPassword == psw.repeatNewPassword:
                result = Conn().updatePassword(userID, hashed_password, Authorize().hashPassword(psw.newPassword))
            else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                result = "Passwords doesn't match."
        else:
                response.status_code = status.HTTP_400_BAD_REQUEST
                result = "Old password doesn't fit."
        return {'message': result}
        
    @api.patch("/storage", summary="Update storage")
    async def updateStorage(storageID: int, storage: Storage, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating a storage. """
        result = Conn().updateStorage(storageID, storage.storageName)
        return {'message': result}

    @api.patch("/placement", summary="Update storage placement")
    async def updatePlacement(placementID: int, placement: UpdateStoragePlacement, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating a placement. """
        columsToUpdate = []
        values = []
        # If values isn't none add them to list.
        if placement.shelf:
            columsToUpdate.append("shelf")
            values.append(placement.shelf)
        if placement.row:
            columsToUpdate.append("row")
            values.append(placement.row)
        if placement.storageID:
            columsToUpdate.append("storageID")
            values.append(placement.storageID)

        result = Conn().updatePlacement(placementID, columsToUpdate, values)
        if result == "Something went wrong":
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": result}

    @api.patch("/artefactType", summary="Update an artefact type")
    async def updateArtefactType(artefactTypeID: int, aType: ArtefactType, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating an artefact type. """
        result = Conn().updateArtefactType(artefactTypeID, aType.artefactType)
        return {'message': result}

    @api.patch("/artefact", summary="Update artefact")
    async def updateArtefact(artefactID: int, artefact: UpdateArtefact, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating an artefact. """
        columsToUpdate = []
        values = []
    
        # If values isn't none add them to list.
        if artefact.artefact:
            columsToUpdate.append("artefact")
            values.append(artefact.artefact)
        if artefact.artefactDescription:
            columsToUpdate.append("artefactDescription")
            values.append(artefact.artefactDescription)
        if artefact.artefactTypeID:
            columsToUpdate.append("artefactTypeID")
            values.append(artefact.artefactTypeID)
        if artefact.placementID:
            columsToUpdate.append("placementID")
            values.append(artefact.placementID)

        result = Conn().updateArtefact(artefactID, columsToUpdate, values)
        if result == "Something went wrong":
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": result}

    @api.patch("/logType", summary="Update an log type")
    async def updateLogType(logTypeID: int, lType: LogType, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating an log type. """
        result = Conn().updateLogType(logTypeID, lType.logType)
        return {'message': result}

    @api.patch("/controller", summary="Update controller")
    async def updateController(controllerID: int, cntr: UpdateController, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating a controller. """
        columsToUpdate = []
        values = []
    
        # If values isn't none add them to list.
        if cntr.controller:
            columsToUpdate.append("controller")
            values.append(cntr.controller)
        if cntr.storage:
            columsToUpdate.append("storage")
            values.append(cntr.storage)

        result = Conn().updateController(controllerID, columsToUpdate, values)
        if result == "Something went wrong":
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": result}

    # -------------------------------------- DELETE -------------------------------------- #
    
    @api.delete("/employeeType", summary="Delete employee type")
    async def deleteEmployeeType(employeeTypeID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting an employee type. """
        Conn().deleteEmployeeType(employeeTypeID)
        return {"message": "Deleted employee type"}

    @api.delete("/user", summary="Delete user")
    async def deleteUser(userID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting a user. """
        Conn().deleteUser(userID)
        return {"message": "Deleted user"}
        
    @api.delete("/storage", summary="Delete storage")
    async def deleteStorage(storageID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleint a storage. """
        Conn().deleteStorage(storageID)
        return {"message": "Deleted storage"}

    @api.delete("/placement", summary="Delete placement")
    async def deletePlacement(placementID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting placement. """
        Conn().deletePlacement(placementID)
        return {"message": "Deleted placement"}
        
    @api.delete("/artefactType", summary="Delete artefact type")
    async def deleteArtefactType(artefactTypeID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting artefact type. """
        Conn().deleteArtefactType(artefactTypeID)
        return {"message": "Deleted artefactType"}

    @api.delete("/artefact", summary="Delete artefact")
    async def deleteArtefact(artefactID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting artefact. """
        Conn().deleteArtefact(artefactID)
        return {"message": "Deleted artefact"}

    @api.delete("/logType", summary="Delete log type")
    async def deleteLogType(logTypeID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting log type. """
        Conn().deleteLogType(logTypeID)
        return {"message": "Deleted logType"}

    @api.delete("/controller", summary="Delete controller")
    async def deleteController(controllerID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting controller. """
        Conn().deleteController(controllerID)
        return {"message": "Deleted controller"}

    @api.delete("/log", summary="Delete log")
    async def deleteLog(logID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting log. """
        Conn().deleteLog(logID)
        return {"message": "Deleted log"}

uvicorn.run(Archaeologygallery().api, host='0.0.0.0', port=8000)