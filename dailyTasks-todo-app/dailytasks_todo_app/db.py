from sqlmodel import SQLModel, create_engine, Session
from dailytasks_todo_app import setting

connection_string: str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
# connections are stand_by, we don't have to create new connection every time
engine = create_engine(
    connection_string, 
    connect_args= {"sslmode":"require"}, 
    pool_recycle= 300,
    pool_size= 10,
    )


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    # using with syntax we don't have to worry about closing of sessions
    with Session(engine) as session:
        yield session

