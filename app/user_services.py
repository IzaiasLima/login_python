from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config
from app.db.models import UserModel
from app.schemas import User


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

crypt_context = CryptContext(schemes=["sha256_crypt"])

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid access token",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_usr_or_pass = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid username or password",
)

insufficient_permissions = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User don't have necessary permissions.",
)

user_already_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
)


class UserServices:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def as_dict(self, rows):
        dados = [row._asdict() for row in rows]
        return dados

    def get_user(self, username):
        user_on_db = (
            self.db_session.query(UserModel).filter_by(username=username).first()
        )
        return user_on_db

    def get_users_list(self):
        users = self.db_session.query(UserModel.id, UserModel.username).all()
        return self.as_dict(users)

    def user_register(self, user: User):
        user_model = UserModel(
            username=user.username, password=crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise user_already_exists

    def user_login(self, user: User, expires_in: int = 30):
        db_user = self.get_user(user.username)

        if db_user is None:
            raise invalid_usr_or_pass

        if not crypt_context.verify(user.password, db_user.password):
            raise invalid_usr_or_pass

        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        payload = {"sub": user.username, "exp": exp}
        encoded_payload = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        access_token = {"access_token": encoded_payload, "exp": exp.isoformat()}
        return access_token

    def get_user_on_token(authorization):
        if authorization and authorization.startswith("Bearer "):
            access_token = authorization.split(" ")[1]

            try:
                decoded_token = jwt.decode(
                    access_token, SECRET_KEY, algorithms=[ALGORITHM]
                )
            except JWTError:
                raise invalid_token

            user = decoded_token["sub"]

            if user is None:
                raise invalid_token

        return user

    def verify_admin(self, access_token):
        try:
            decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise invalid_token
        user = self.get_user(decoded_token["sub"])

        if user is None or user.username != "admin":
            raise insufficient_permissions

    def verify_token(self, access_token):
        try:
            decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise invalid_token

        user = self.get_user(decoded_token["sub"])

        if user is None:
            raise invalid_token
