# IMPORTS.
# Libaries / Frameworks.
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Own files.
import secret as s
from connection import Connection as Conn

class Authorize:
    # Scheme that method validateJWT depends on.
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Login", scheme_name="JWT")

    # Initial method, set variables.
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.ALGORITHM = "HS256"

    # Verify if password is correct.
    def verifyPassword(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # Hash a new password.
    def hashPassword(self, password):
        return self.pwd_context.hash(password)

    # Get user with username, and use verifyPassword method, to authenticate the user.
    def authenticateUser(self, username: str, password: str):
        # Get user from database.
        user = Conn().login(username)
        # Make sure user isn't none.
        if user is not None:
            # If result from verifyPassword method is true..
            if self.verifyPassword(password, user[2]):
                # ..Return the user.
                return user
        # Return false if something one of the if statements failed.
        return False

    # Create the JWT.
    def createAccessToken(self, data: dict, expires_delta: timedelta | None = None):
        # Create copy of data dict.
        to_encode = data.copy()
        # if expires_delta is not none..
        if expires_delta:
            # ..Set expire to now + expires_delta.
            expire = datetime.utcnow() + expires_delta
        # Otherwise..
        else:
            # ..Set expire to now + 15 minutes.
            expire = datetime.utcnow() + timedelta(minutes=15)
        # Add expire to the copied dict.
        to_encode.update({"exp": expire})

        # Encode the dict to a JWT and return it.
        return jwt.encode(to_encode, s.SECRET_KEY, algorithm=self.ALGORITHM)

    
    # Validate the JWT.
    async def validateJWT(self, token: str = Depends(oauth2_scheme)):
        # Make exception, for if credentials can not be validated.
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # Try to..
        try:
            # ..Decode the JWT, and put data into payload.
            payload = jwt.decode(token, s.SECRET_KEY, algorithms=[self.ALGORITHM])
            # Get username from payload.
            username: str = payload.get("sub")
            # if the username is none...
            if username is None:
                # ..Raise the custom exception.
                raise credentials_exception
        # And if it fails...
        except JWTError:
            # ..Raise the custom exception.
            raise credentials_exception
        # Return true, if nothing went wrong.
        return True