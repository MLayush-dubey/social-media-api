from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2



router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()  #searches by email from the database and stores the entire row in user variable
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):  #database pswd contains hashed pswd(user.password), user_credentials is basically input user pswd
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #once both are verified--> create JWT token containing the user id
    user_token = oauth2.create_token(data={"user_id": user.id})  #user.id grabs id from user row which we extracted above
    #return token
    return {"user_token": user_token, "token_type": "bearer"}
