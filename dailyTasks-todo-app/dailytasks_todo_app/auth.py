from passlib.context import CryptContext
from sqlmodel import Session, select
from typing import Annotated
from dailytasks_todo_app.db import get_session
from fastapi import Depends, HTTPException, status
from dailytasks_todo_app.models import User, Todo, TokenData, Refresh_TokenData
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta




SECRET_KEY = "9f5cd4e92e83cae9465101dc0436d7ff21609c1bdcbf059c0af75f7392d81b70"
ALGORITHYM = "HS256"
EXPIRY_TIME = 15


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes="bcrypt")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# this function search from the database, if the username as well as the email exists.
def get_user_from_db(session: Annotated[Session, Depends(get_session)], 
                     username: str | None = None, 
                     email: str | None = None):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if user:
            return user
    return user
    
# user authentication
def authenticate_user(session: Annotated[Session, Depends(get_session)],
                      username: str,
                      password: str):
    db_user = get_user_from_db(session= session, username=username, email=username)
    if not db_user:
        return False
    if not verify_password(password=password, hashed_password=db_user.password):
        return False
    return db_user
    
    
def create_access_token(data: dict, expiry_time: timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # jwt token needs a key to store expiry time i.e. exp
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHYM)
    return encoded_jwt
    
    
def current_user(token: Annotated[str, Depends(oauth_scheme)],
                 session: Annotated[Session, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError: 
        raise credentials_exception
    
    user = get_user_from_db(session, username=token_data.username)
    if not user:
        raise credentials_exception
    return user
    
# copied from create_access_token
def create_refresh_token(data: dict, expiry_time: timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # jwt token needs a key to store expiry time i.e. exp
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHYM)
    return encoded_jwt
    
    
# copied from current_user
# refresh token will be created from email
def validate_refresh_token(token: Annotated[str, Depends(oauth_scheme)],
                           session: Annotated[Session, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = Refresh_TokenData(email=email)
    except JWTError: 
        raise credentials_exception
    
    user = get_user_from_db(session, email=token_data.email)
    if not user:
        raise credentials_exception
    return user

    