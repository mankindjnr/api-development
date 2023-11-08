from fastapi import FastAPI, Request, Response, status, APIRouter, Depends, HTTPException
from .. import models, database, schemas, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends
    (oauth2.get_current_user)):

    post_exists = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    liked_post = vote_query.first()

    if (vote.direction == 1):
        if liked_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already liked this post")
        
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()

        return {"detail": "Post liked"}
    else:
        if not liked_post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You haven't liked this post")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"detail": "Post unliked"}