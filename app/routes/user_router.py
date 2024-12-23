from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.user_services import UserServices
from app.schemas import User
import urllib.parse as html
import json

user = APIRouter(prefix="/user")


async def get_body(req: Request):
    payload = await req.body()
    payload = payload.decode("utf8")
    payload = html.unquote(payload)

    try:
        body = json.loads(payload)
    except:
        try:
            lista = list(payload.split("&"))
            body = dict(l.split("=") for l in lista)
        except:
            body = {}

    return body


@user.post("/register")
def user_register(
    form_data=Depends(get_body),
    db_session: Session = Depends(get_db_session),
):
    service = UserServices(db_session=db_session)
    service.user_register(form_data)
    return JSONResponse(
        content={"message": "Login success"}, status_code=status.HTTP_201_CREATED
    )


@user.post("/login")
def user_register(
    form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    service = UserServices(db_session=db_session)
    user = User(username=form_user.username, password=form_user.password)
    jwt_token = service.user_login(user=user)

    html = '<button type="button" hx-get="/user/logout">Logout</button>'
    response = HTMLResponse(html, status_code=status.HTTP_200_OK)

    response.set_cookie(
        key="access_token",
        value="Bearer {}".format(jsonable_encoder(jwt_token)),
        httponly=True,
        secure=True,
        max_age=(2 * 3600),
        expires=(2 * 3600),
        samesite="lax",
        path="/",  # para o site todo
    )
    return response


@user.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = HTMLResponse("<script>location.href='/pages/login.html'</script>")
    response.delete_cookie("access_token")
    return response
