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
        accessToken = Authorize().createAccessToken(data={"sub": user[1]}, expires_delta=access_token_expires)

        content = {"Message": "You've logged in."}
        headers = {"Authorization": f"Bearer {accessToken}"}
        return JSONResponse(content=content, headers=headers)
    
    # READ
        # If the artefactID isn't none.
        if artefactID:
            title = "Artefact"
            result

        else:
            title = "Artefacts"
            result
    
        return {title: result}

    # UPDATE

    # DELETE
    

uvicorn.run(Archaeologygallery().api, host='0.0.0.0', port=8000)