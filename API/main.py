# IMPORTS.
# Libaries / Frameworks.
import datetime
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

# Own files.
from connection import Connection as Conn
from authorize import Authorize
from basemodels import *

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
    async def addEmployeeType(employeeType: EmployeeType, response: Response, token: Token = Depends(Authorize().validateJWT)):
        """ Endpoint for creating a new user. """
        Conn().insertEmployeeType(employeeType)
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

    # --------------------------------------- READ --------------------------------------- #

    @api.get("/user", summary="Get all or one user")
    def getUser(userID: int = None, token: Token = Depends(Authorize().validateJWT)):
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
    def getPostal(postal: int = None, token: Token = Depends(Authorize().validateJWT)):
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
    def getStorage(storageID: int = None, token: Token = Depends(Authorize().validateJWT)):
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
    def getPlacement(placementID: int = None, token: Token = Depends(Authorize().validateJWT)):
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
    def getArtefactType(artefactTypeID: int = None, token: Token = Depends(Authorize().validateJWT)):
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
    def getArtefact(artefactID: int = None, token: Token = Depends(Authorize().validateJWT)):
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

    # -------------------------------------- UPDATE -------------------------------------- #

    @api.patch("/user", summary="Update user")
    def updateUser(userID: int, user: UpdateUser, token: Token = Depends(Authorize().validateJWT)):
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
        if user.employeeTypeID:
            columsToUpdate.append("employeeTypeID")
            values.append(user.employeeTypeID)

        result = Conn().updateUser(userID, columsToUpdate, values)
        if result == "Something went wrong":
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": result}

    @api.patch("/password", summary="Update user password")
    def updatePassword(userID: int, psw: UpdatePsw, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating a users password. """
        if psw.newPassword == psw.repeatNewPassword:
            result = Conn().updatePassword(userID, psw.oldPassword, psw.newPassword)
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            result = "Passwords doesn't match."
        return {'message': result}
        
    @api.patch("/storage", summary="Update storage")
    def updateStorage(storageID: int, storage: Storage, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating a storage. """
        result = Conn().updateStorage(storageID, storage.storageName)
        return {'message': result}

    @api.patch("/placement", summary="Update storage placement")
    def updatePlacement(placementID: int, placement: UpdateStoragePlacement, token: Token = Depends(Authorize().validateJWT)):
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
    def updateArtefactType(artefactTypeID: int, aType: ArtefactType, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for updating an artefact type. """
        result = Conn().updateArtefactType(artefactTypeID, aType.artefactType)
        return {'message': result}

    @api.patch("/artefact", summary="Update artefact")
    def updateArtefact(artefactID: int, artefact: UpdateArtefact, token: Token = Depends(Authorize().validateJWT)):
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

    # -------------------------------------- DELETE -------------------------------------- #
    
    @api.delete("/user", summary="Delete user")
    def getUser(userID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting a user. """
        
    @api.delete("/storage", summary="Delete storage")
    def getStorage(storageID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleint a storage. """

    @api.delete("/placement", summary="Delete placement")
    def getPlacement(placementID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting placement. """
        
    @api.delete("/artefactType", summary="Delete artefact type")
    def getArtefactType(artefactTypeID: int, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting artefact type. """

    @api.delete("/artefact", summary="Delete artefact")
    def getArtefact(artefactID: int = None, token: Token = Depends(Authorize().validateJWT)):
        """ Endpont for deleting artefact. """

uvicorn.run(Archaeologygallery().api, host='0.0.0.0', port=8000)