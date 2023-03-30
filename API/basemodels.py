from pydantic import BaseModel

# BASEMODELS
class Token(BaseModel):
    """ Response body for the token. """
    accessToken: str

class EmployeeType(BaseModel):
    """ Request body when adding new employee type. """
    employeeType: str

class User(BaseModel):
    """ Request body when adding new user. """
    firstName: str
    lastName: str
    email: str
    password: str
    doorCode: int
    phoneNumber: int
    address: str
    postal: int
    employeeTypeID: int

class UpdateUser(BaseModel):
    """ Request body when updating user. """
    firstName: str = None
    lastName: str = None
    email: str = None
    phoneNumber: int = None
    address: str = None
    postal: int = None
    employeeTypeID: int = None

class UpdatePsw(BaseModel):
    """ Request body when updating password. """
    oldPassword: str
    newPassword: str
    repeatNewPassword: str

class Storage(BaseModel):
    """ Request body when adding or updating a storage room. """
    storageName: str

class StoragePlacement(BaseModel):
    """ Request body when adding a new storage placement. """
    shelf: int
    row: str
    storageID: int

class UpdateStoragePlacement(BaseModel):
    """ Request body when updating a storage placement. """
    shelf: int = None
    row: str = None
    storageID: int = None

class ArtefactType(BaseModel):
    """ Request body when adding or updating a artefact type. """
    artefactType: str

class Artefact(BaseModel):
    """ Request body when adding a new artefact. """
    artefact: str
    artefactDescription: str
    artefactTypeID: int
    placementID: int

class UpdateArtefact(BaseModel):
    """ Request body when updating a artefact. """
    artefact: str = None
    artefactDescription: str = None
    artefactTypeID: int = None
    placementID: int = None