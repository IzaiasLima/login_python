from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.connection import DBSession
from app.user_services import UserServices


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_db_session():
    try:
        session = DBSession()
        yield session
    finally:
        session.close()

def current_user(db_session: Session = Depends(get_db_session), access_token = Depends(oauth_scheme)):
    service = UserServices(db_session)
    user = service.verify_token(access_token)
    return user.username

def token_verifier(db_session: Session = Depends(get_db_session), access_token = Depends(oauth_scheme)):
    service = UserServices(db_session)
    service.verify_token(access_token)

def admin_verifier(db_session: Session = Depends(get_db_session), access_token = Depends(oauth_scheme)):
    service = UserServices(db_session)
    service.verify_admin(access_token)
