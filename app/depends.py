from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.connection import DBSession
from app.user_services import UserServices


def get_db_session():
    try:
        session = DBSession()
        yield session
    finally:
        session.close()


def token_verifier(request: Request, db_session: Session = Depends(get_db_session)):
    access_token = request.cookies.get("access_token")
    service = UserServices(db_session)
    return service.verify_token(access_token)


def admin_verifier(request: Request, db_session: Session = Depends(get_db_session)):
    token = token_verifier(request)
    service = UserServices(db_session)
    service.verify_user_admin(token)
