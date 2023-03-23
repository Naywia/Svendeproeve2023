# IMPORTS.
# Libaries / Frameworks.
import datetime
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

# Own files.
from connection import Connection as Conn
from authorize import Authorize

# BASEMODELS
# Response body
class Token(BaseModel):
    accessToken: str

# API
class Archaeologygallery:
    # Make variable for the api.
    api = FastAPI() 

    # Get access token.
    @api.post("/Login", summary="Login")
    async def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
    
    #token: Token = Depends(Authorize().validateJWT)

    # test
    @api.get("/Test", summary="Test the api connection.")
    def test():
        return {"Hello": "World!"}

    # UPDATE

    # DELETE
    

uvicorn.run(Archaeologygallery().api, host='0.0.0.0', port=8000)