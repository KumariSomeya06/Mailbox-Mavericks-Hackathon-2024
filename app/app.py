from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class User(BaseModel):
    name: str
    email: str
@app.post("/user/")
def create_user(user: User):
    return {"message": f"User {user.name} with email {user.email} created successfully."}
