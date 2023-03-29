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
    employeeTypeID: int

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