from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth, votes
from fastapi.middleware.cors import CORSMiddleware



models.Base.metadata.create_all(bind=engine) # This line creates the tables in the database based on the models defined in the models.py file. 
# It uses the metadata of the Base class to create the tables and binds it to the engine that connects to the database.


app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") # get here is the http method that the user should use. This get method means that we have to send a get request to our api.
async def root(): # regular function, async here is optional it is only necessary when we are preforming any asynchronous tasks.
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

