from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import database, models, schemas, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=["VOTE"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    #if user searches for a post that does not exist logic
    post = db.query(models.Post).filter(models.Post.id == vote.posts_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {vote.posts_id} does not exist")

    #checking if the user vote already exists in a post or not-->Validates if current user id matches the user id of the table AND posts_id matches the table's post id
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.posts_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):  #if user has already liked on a post then this will be executed

        if found_vote:  #if like already exists then this will be executed
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.posts_id}")
        

        #if like does not exist we will add the like
        new_vote = models.Votes(post_id = vote.posts_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:  #if user's votes is 0(unlike)
        if not found_vote:  #if vote exist hi nahi krta meaning neither 0 or 1 then this will be run
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)   #remove the vote if it exists(meaning like h toh unlike krdo)
        db.commit()

        return {"message": "successfully deleted vote"} 

        
