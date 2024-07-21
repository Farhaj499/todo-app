from fastapi import APIRouter
from typing import Annotated
from dailytasks_todo_app.models import Register_User, User
from fastapi import Depends
from dailytasks_todo_app.auth import get_user_from_db, hash_password, oauth_scheme, current_user
from dailytasks_todo_app.db import get_session
from sqlmodel import Session

# if user sends a request, then it will go to user_router
user_router = APIRouter(
    prefix = "/user",
    tags = ["user"],
    responses = {404: {"description": "Not found"}}
)

@user_router.get("/")
async def read_user():
    return {"message": "Welcome to dailyTasks todo app User page"}

@user_router.get("/register")
async def register_user(new_user: Annotated[Register_User, Depends()],
                        session: Annotated[Session, Depends(get_session)]):
    db_user = get_user_from_db(session, new_user.username, new_user.email)
    if db_user:
        raise HTTPException(status_code= 409, detail= "User already exists. Please enter a different email or username")
    user = User(username = new_user.username,
                email = new_user.email,
                password = hash_password(new_user.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f"""User {user.username} registered  successfully"""}


@user_router.get("/me")
async def user_profile(current_user: Annotated[User, Depends(current_user)]):
    return current_user



