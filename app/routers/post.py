from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import schemas
from schemas import PostOut
from database import get_db
from models import Post, Vote
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from typing import List, Optional
import oauth2


router = APIRouter(
    prefix= "/posts",
    tags = ['Posts']
)



# Path operation or route
# This is a path operation decorator. It tells FastAPI that the function 
# below is in charge of handling requests that go to the path / and 
# use the GET method.



# @router.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     result = db.execute(select(Post))
#     posts = result.scalars().all()
#     return posts


@router.get("/", response_model= list[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), skip: int = 0, limit: int = 10, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # select_posts_query = db.execute(select(Post).filter(Post.title.contains(search)).offset(skip).limit(limit))
    posts = db.execute(
        select(
            Post,
            func.count(Vote.post_id).label("votes")
        ).outerjoin(Vote, Vote.post_id == Post.id).group_by(Post.id)
        .filter(Post.title.contains(search)).offset(skip).limit(limit)).all()
    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse) # This line defines a POST endpoint at the path /posts. The status_code parameter indicates that a successful creation of a post will return a 201 Created status code.
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # This line defines the function that will handle the POST request. The post parameter is expected to be of type PostFormat, which is a Pydantic model that validates the incoming request data.
    # cursor.execute("""Insert INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # # We use parameterized queries to prevent SQL injection attacks. 
    # # The %s placeholders are used to safely insert the values of post.title, post.content, and post.published into the SQL query.
    
    # new_post = cursor.fetchone()
    # conn.commit() # This line commits the transaction to the database, ensuring that the new post is saved.
    # new_post = Post(title=post.title, content=post.content, published=post.published) 
    new_post = Post(owner_id = current_user.id, **post.model_dump()) # This line creates a new instance of the Post model using the data from the incoming request. The **post.model_dump() syntax unpacks the validated data from the Pydantic model into keyword arguments for the Post constructor.
    db.add(new_post) # This line adds the new_post object to the database session. It prepares the new post to be inserted into the database.
    db.commit() # This line commits the transaction to the database, ensuring that the new post is saved.
    db.refresh(new_post) # This line refreshes the new_post object with the data from the database, including any auto-generated fields like the ID. This ensures that the new_post object contains the most up-to-date information after being inserted into the database.

    return new_post # This line returns a dictionary with a single key 'data', whose value is the post_dict. This is the response that will be sent back to the client when they make a POST request to the /posts endpoint.


        
@router.get("/{id}", response_model= schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.execute(
        select(
            Post,
            func.count(Vote.post_id).label("votes")
        ).outerjoin(Vote, Vote.post_id == Post.id).group_by(Post.id).where(Post.id == id)).first()
    # post = result.scalar()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    deleted_post = db.execute(select(Post).where(Post.id == id)).scalars().first()
        
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATe posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post = db.execute(
            update(Post)
            .where(Post.id == id)
            .values(**post.model_dump())
            .returning(Post)
        ).scalar_one_or_none()   
     
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if updated_post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
        
    
    db.commit()
    return updated_post