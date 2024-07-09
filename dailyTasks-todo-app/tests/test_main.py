from fastapi.testclient import TestClient
from fastapi import FastAPI
from dailytasks_todo_app import setting
from sqlmodel import SQLModel, create_engine, Session
from dailytasks_todo_app.main import app, get_session
import pytest

# creating engine to establish connection with database
connection_string: str = str(setting.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg")
# connections are stand_by, we don't have to create new connection every time
engine = create_engine(
    connection_string, 
    connect_args= {"sslmode":"require"}, 
    pool_recycle= 300,
    pool_size= 10,
    echo= True
    )

#===========================================================================

# Refracting code using pytest fixture

# scope="module" will tell this fixture will run for whole module(for all tests)
# scope="function" will tell this fixture will run for every test
# autouse will automatically call every test

    # Steps:  
    # 1-Arrange: Arrange Resources (tables)
    # 2-Act: Executing functions
    # 3-Assert: Verifying results
    # 4-Cleanup: Cleaning up resources

@pytest.fixture(scope="module", autouse=True)
def get_db_session():    
    SQLModel.metadata.create_all(engine)
    yield Session(engine)    

# test_app fixture will be called after get_db_session
@pytest.fixture(scope="function")
def test_app(get_db_session):
    def test_session():
        yield get_db_session
    app.dependency_overrides[get_session] = test_session
    with TestClient(app= app) as client:
        yield client
#===========================================================================


# Test 1 : Root testing 
def test_root():
    # if in main.py, name of our app is xyz, then we can write app= xyz
    client =  TestClient(app= app)
    response = client.get("/")
    data  = response.json()
    assert response.status_code == 200
    # if true then no assert,
    # if false, it will raise an exception of assert error
    assert data == {"message": "Welcome to dailyTasks-todo-app"}


# Test 2 :POST Testing
def test_create_todos(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     # below function will over-write the default session
    #     def db_session_override():
    #         return session
    # # it will test the session logic in main file
    # # also the database created will be connected to test branch
    # app.dependency_overrides[get_session] = db_session_override
    # client = TestClient(app= app)
    
    test_todo = {"content": "TODO for testing", "is_completed": False}
    response = test_app.post("/todos", json=test_todo)
    data = response.json()
    assert response.status_code == 200
    assert data["content"] == test_todo["content"] 


# Test 3 : Getting all todos
def test_get_all_todos(test_app):
    test_todo = {"content": "get all Todo for testing", "is_completed": False}
    postResponse = test_app.post("/todos", json=test_todo)
    
    response = test_app.get("/todos")
    todos_list = response.json()[-1]
    assert response.status_code == 200
    assert todos_list["content"] == test_todo["content"]


# Test 4 : Get single todo
def test_get_single_todo(test_app):
    test_todo = {"content": "get Single todo for testing", "is_completed": False}
    postResponse = test_app.post("/todos", json=test_todo)
    todo_id = postResponse.json()["id"]
    
    response = test_app.get(f"/todos/{todo_id}")
    data  = response.json()
    assert response.status_code == 200
    assert data["content"] == test_todo["content"]


# Test 5 : Edit todo
def test_edit_todo(test_app):
    test_todo = {"content": "New todo for testing", "is_completed": False}
    postResponse = test_app.post("/todos/", json=test_todo)
    todo_id = postResponse.json()["id"]
    
    edited_todo = {"content": "Edited todo for testing", "is_completed": False}
    response = test_app.put(f"/todos/{todo_id}", json=edited_todo)
    data  = response.json()
    assert response.status_code == 200
    assert data["content"] == edited_todo["content"]


# Test 6 : Delete todo
def test_delete_todo(test_app):
    test_todo = {"content": "Delete todo for testing", "is_completed": False}
    postResponse = test_app.post("/todos/", json=test_todo)
    todo_id = postResponse.json()["id"]
    
    response = test_app.delete(f"/todos/{todo_id}")
    data  = response.json()
    assert response.status_code == 200


