import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings 

oauth2scheme = OAuth2PasswordBearer('login')  #we pass in the path operation that is needed 

#we need 3 pieces of info--> SecretKey, Algorithm, expiration time
SECRET_KEY = settings.secret_key  #RANDOM STRING
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_token(data:dict):   
    to_encode = data.copy()   #payload creation

    #creating expiration date for token
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify__access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")  #this user_id is from auth.py
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except PyJWTError:
        raise credentials_exception
    


def get_current_user(token: str = Depends(oauth2scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
                                          , headers={"WWW-Authenticate": "Bearer"})
    
    token = verify__access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user