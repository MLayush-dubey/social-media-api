from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

#inheriting class
class CreatePost(PostBase):
    pass   #inherits as-it-is\


class ResponsePost(PostBase):    #deriving from above pydantic base model
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:    #since pydantic models only run dictionaries, this method will tell fastAPI to run it even if its ORM
        orm_mode=True



class PostOut(BaseModel):
    Post: ResponsePost  # Capital P se "Post" rakho (singular, not "Posts")
    votes: int

    class Config:
        orm_mode = True




#this is what will be shown to the client
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    






class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    user_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None



#creating voting schemas
class Vote(BaseModel):
    posts_id: int
    dir: int = Field(ge=0, le=1)  #less than 1


