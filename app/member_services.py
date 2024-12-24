from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError

from decouple import config
from app.db.models import MembersModel


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

crypt_context = CryptContext(schemes=["sha256_crypt"])

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_usr_or_pass = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
)

insufficient_permissions = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User insufficient permission",
)

user_already_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
)


invalid_fields_len = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="All fields must be filled in"
)

invalid_user_name = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user name"
)


class MemberServices:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def as_dict(self, rows):
        dados = [row._asdict() for row in rows]
        return dados

    # registrar membro no sistema
    def member_register(self, user, form_data):
        if (len(form_data) < 15):
            raise invalid_fields_len
        
        member_model = MembersModel()
        member_model.from_dict(form_data)

        try:
            self.db_session.add(member_model)
            self.db_session.commit()
        except IntegrityError as e:
            print(e)
            raise user_already_exists
