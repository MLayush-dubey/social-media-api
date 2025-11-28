from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Depends
from .. import models, schemas, oauth2  #singledot--> main dir, doubledot--> parent directory, dir k andhar dir
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['Posts']   #used for grouping API endpoints in automatically generated documentation(SwaggerUI)
)




@router.get('/', response_model=List[schemas.PostOut])     #to retrieve data, we usually use GET http method
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    print(search)
    print(limit)
    #retrieve_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #this returns list of all the post objects, hence we used List above
    #by addind owner_id we are explicitly only returning posts made by the current user
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes"))\
    .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
    .group_by(models.Post.id)\
    .filter(models.Post.title.contains(search))\
    .limit(limit)\
    .offset(skip).all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_posts(new_post:schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):          #it automatically checks the parameters of the class Post(defines schema)
    #NOTE:cursor.execute("""INSERT INTO posts (title, content, published) VALUES({posts.title}, {posts.content}, {posts.published})""")--> should be avoided to prevent SQL injection
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                 (new_post.title, new_post.content, new_post.published))
    # new_posts = cursor.fetchone()
    
    # conn.commit()
    #print(**new_post.model_dump())   #NOTE:unpacking the dictionary this way we dont have to write new_post.title, new_post.content, new_post.published
 
    new_posts = models.Post(owner_id=current_user.id,**new_post.model_dump())
    db.add(new_posts)   #adds the new post to the database
    db.commit()   #commits to the database
    db.refresh(new_posts)   #shows the new post in the database(RETURNING * IN THE SQL QUERY)
    return new_posts    #this prints it to postman(frontend/client)


@router.get("/latest")
def latest_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    # latest = cursor.fetchone()
    latestpost = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return {"latestposts": latestpost}
#NOTE:APi structuring is very imp, if we had placed this below the id func, it would have failed because fastapi works from top down and would get the
#id first, hence try to convert 'latest' into an int


#to get a single post
@router.get("/{id}", response_model=schemas.PostOut)   #NOTE: this is a path parameter(will be returned as a str)
def get_singlepost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id= %s""", (id,))   #added a comma after id so it can be taken as tuple and not an int(throws an error)
    # singleposts = cursor.fetchone()
    # print(singleposts)
    #singleposts = db.query(models.Post).filter(models.Post.id == id).first() #finds the first matching post with the id

    singleposts = db.query(models.Post, func.count(models.Votes.post_id).label("votes"))\
    .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
    .group_by(models.Post.id).first()

    if not singleposts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    
    #if singleposts.owner_id != current_user.id:   
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to access it")
    
    return singleposts



@router.delete("/{id}", status_code=status.HTTP_200_OK)  #using 204 no content will not return any body if successfully deletion, hence 200 is best practice
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_posts = cursor.fetchone()
    # if deleted_posts==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # conn.commit()
    deleteposts = db.query(models.Post).filter(models.Post.id == id)  #query based deletion
    if deleteposts.first()==None:   #query object can never be None, hence we use .first()  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    #creating if operation such that user can only delete his specific posts and not others
    if deleteposts.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to delete this post")

    deleteposts.delete(synchronize_session=False)   #synchronize session basically tells to not save in-memory
    db.commit()
    return {"data": deleteposts, "detail": f"Post with id: {id} has been successfully deleted"}


@router.put("/{id}", response_model=schemas.ResponsePost)
def update_posts(id: int, update_post: schemas.CreatePost, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", (update_post.title, update_post.content, update_post.published, id))
    # updated_posts = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)  

    updatepost = post_query.first()   #we are storing it here because we cannot update if we add the .first() in post_query, hence we separated it

    if updatepost==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    #creating if statement so the user with specific id can only update his specific posts
    if updatepost.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to update this post")
    
    post_query.update(update_post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()