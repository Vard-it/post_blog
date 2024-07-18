from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List, Optional

from sqlalchemy import func
from .. import main

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # main.cursor.execute("""SELECT * from posts""")
    # posts = main.cursor.fetchall()

    results_query = ((db.query(models.Post, func.count(models.Vote.post_id).label("votes")).
               join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)).group_by(models.Post.id).
               filter(models.Post.title.contains(search)).limit(limit).offset(skip).all())

    try:
        query_results = (
            db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
            .group_by(models.Post.id)
            .filter(models.Post.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )

        # Transform results to match the response schema
        results = [
            schemas.PostOut(
                title=post.title,
                content=post.content,
                published=post.published,
                post_id=post.id,
                votes=votes  # or any other field required by PostOut
            )
            for post, votes in query_results
        ]

        return results
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/create-post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""",
    #                (post.title, post.content))
    #
    # new_post = cursor.fetchone()
    # conn.commit()

    #new_post = models.Post(title=post.title, content=post.content, published=True)  #just a query, vorpeszi sti 50 angam kirinq vech post.title kam post.urishban dra hamar posty sarqumnq dict
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    # returning *
    db.refresh(new_post)

    return new_post


@router.get("/get-post/{id}", response_model=schemas.Post)
def get_post_by_id(id: int, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE post_id = %s""", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} id was not found.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return post


@router.delete("/delete-post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE post_id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} id does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)  #You can read about it at session basics documentation
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/update-post/{id}", response_model=schemas.Post)
def update_post_by_id(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s  WHERE post_id = %s RETURNING *""",
    #                (post.title, post.content, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} id does not exist")
    post = post_query.first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    updated_postik = db.query(models.Post).filter(models.Post.id == id).first()

    return updated_postik
