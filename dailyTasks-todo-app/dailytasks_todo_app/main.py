from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from dailytasks_todo_app import setting
from typing import Annotated
from contextlib import asynccontextmanager



# creating model
    # data model: if simply need to validate data
    # tabel model: if need to create table
    # in SQLModel, we can use both above models
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True, min_length=3, max_length=54)
    is_completed: bool = Field(default=False)

# creating engine to establish connection with database
# one engine for whole application
connection_string: str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
# connections are stand_by, we don't have to create new connection every time
engine = create_engine(
    connection_string, 
    connect_args= {"sslmode":"require"}, 
    pool_recycle= 300,
    pool_size= 10,
    echo= True
    )

def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    # using with syntax we don't have to worry about closing of sessions
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifeSpan(app: FastAPI):
    print("Creating tables") 
    create_tables()
    print("Tables created")
    yield

app : FastAPI = FastAPI(lifespan= lifeSpan, title= "Todo App", version= "0.1.0", description= "Simple todo app")







@app.get("/")

# when get a request on "/", run below function
async def root():
    return {"message": "Welcome to dailyTasks-todo-app"}

# creating a new task
# with response_model, every todo is validated
@app.post("/todos/", response_model=Todo)
async def create_todos(todo: Todo, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todos/", response_model=list[Todo])
async def get_all_todos(session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo)
    todos= session.exec(statement).all()
    if (todos):
        return todos
    else:
        raise HTTPException(status_code= 404, detail= "Task not found")
    

@app.get("/todos/{id}", response_model=Todo)
async def get_single_todo(id: int ,session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo).where(Todo.id == id)
    todo= session.exec(statement).first()
    if (todo):
        return todo
    else:
        raise HTTPException(status_code= 404, detail= "Task not found")

@app.put("/todos/{id}", response_model=Todo)
async def edit_todo(id: int, todo: Todo, session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo).where(Todo.id == id)
    existing_todo= session.exec(statement).first()
    if(existing_todo):
        existing_todo.content = todo.content
        existing_todo.is_completed = todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException(status_code= 404, detail= "Task not found")

@app.delete("/todos/{id}")
async def delete_todo(id: int, session: Annotated[Session, Depends(get_session)]):
    statement = select(Todo).where(Todo.id == id)
    existing_todo= session.exec(statement).first()
    if(existing_todo):
        session.delete(existing_todo)
        session.commit()
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(status_code= 404, detail= "Task not found") 

