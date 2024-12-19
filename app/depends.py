from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# from app.db.connection import Session
from app.user_services import UserServices


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


def token_verifier(
    db_session: Session = Depends(get_db_session), access_token=Depends(oauth_scheme)
):
    service = UserServices(db_session)
    service.verify_token(access_token)
