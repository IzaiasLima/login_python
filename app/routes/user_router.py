from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.user_services import UserServices
from app.schemas import User

user= APIRouter(prefix="/user")

@user.post("/register")
def user_register(
    user: User,
    db_session: Session = Depends(get_db_session),
):
    service = UserServices(db_session=db_session)
    service.user_register(user=user)
    return JSONResponse(content={"msg": "success"}, status_code=status.HTTP_201_CREATED)


@user.post("/login")
def user_register(
    request_form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    service = UserServices(db_session=db_session)
    user = User(
        username=request_form_user.username, password=request_form_user.password
    )

    access_token = service.user_login(user=user)
    return JSONResponse(content=access_token, status_code=status.HTTP_200_OK)

