from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Field, create_engine, Session, select
from dailytasks_todo_app import setting
from typing import Annotated
from contextlib import asynccontextmanager
from dailytasks_todo_app.auth import authenticate_user, create_refresh_token, validate_refresh_token
from dailytasks_todo_app.auth import create_access_token, EXPIRY_TIME, current_user
from dailytasks_todo_app.db import get_session, create_tables
from dailytasks_todo_app.models import Todo, Token, Todo_Create, Todo_Edit, User
from dailytasks_todo_app.router.user import user_router







@asynccontextmanager
async def lifeSpan(app: FastAPI):
    print("Creating tables") 
    create_tables()
    print("Tables created")
    yield

app : FastAPI = FastAPI(lifespan= lifeSpan, title= "Todo App", version= "0.1.0", description= "Simple todo app")

app.include_router(router = user_router)





@app.get("/")

# when get a request on "/", run below function
async def root():
    return {"message": "Welcome to dailyTasks-todo-app"}

# creating a new task
# with response_model, every todo is validated
@app.post("/todos/", response_model=Todo)
async def create_todos(current_user: Annotated[User, Depends(current_user)], 
                       todo: Todo_Create, 
                       session: Annotated[Session, Depends(get_session)]):
    new_todo = Todo(content= todo.content,  
                    user_id= current_user.id)
    
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@app.get("/todos/", response_model=list[Todo])
async def get_all_todos(current_user: Annotated[User, Depends(current_user)],
                        session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo).where(Todo.user_id == current_user.id)
    todos= session.exec(statement).all()
    if (todos):
        return todos
    else:
        raise HTTPException(status_code= 404, detail= "Task not found")
    

@app.get("/todos/{id}", response_model=Todo)
async def get_single_todo(id: int ,
                          current_user: Annotated[User, Depends(current_user)],
                          session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo).where(Todo.user_id == current_user.id).where(Todo.id == id)
    todo= session.exec(statement).first()
    if (todo):
        return todo
    else:
        raise HTTPException(status_code= 404, detail= "Task not found")

@app.put("/todos/{id}", response_model=Todo)
async def edit_todo(id: int,
                    current_user: Annotated[User, Depends(current_user)], 
                    todo: Todo_Edit, 
                    session: Annotated[Session, Depends(get_session)]):
    new_todo = Todo(content= todo.content, user_id= current_user.id)
    
    statement = select(Todo).where(Todo.id == id).where(Todo.user_id == current_user.id)
    existing_todo= session.exec(statement).first()
    if(existing_todo):
        existing_todo.content = new_todo.content
        existing_todo.is_completed = new_todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException(status_code= 404, detail= "Task not found")

@app.delete("/todos/{id}")
async def delete_todo(id: int,
                      current_user: Annotated[User, Depends(current_user)],
                      session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo).where(Todo.id == id).where(Todo.user_id == current_user.id)
    existing_todo= session.exec(statement).first()
    if(existing_todo):
        session.delete(existing_todo)
        session.commit()
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code= 404, detail= "Task not found") 


# login
# whenever user logins, we give him a access token for certain period
# so user can access all endpoints using the access token
# oauth gets username and password in the form of formdata
@app.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Annotated[Session, Depends(get_session)]):
    user = authenticate_user(session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code= 401, detail= "Invalid username or password")
    
    expire_time = timedelta(minutes=EXPIRY_TIME)    
    access_token = create_access_token({"sub":form_data.username}, expire_time)
    
    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub": user.email}, refresh_expire_time)
    
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)


@app.post("/token/refresh")
def refresh_token(old_refresh_token: str,
                  session: Annotated[Session, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"},
    )
    user = validate_refresh_token(old_refresh_token, session)
    if not user:
        raise credentials_exception
    
    expire_time = timedelta(minutes=EXPIRY_TIME)    
    access_token = create_access_token({"sub": user.username}, expire_time)
    
    refresh_expire_time = timedelta(days=7)
    refresh_token = create_refresh_token({"sub": user.email}, refresh_expire_time)

    return Token(access_token= access_token, token_type="bearer", refresh_token= refresh_token)






