from typing import Optional
from fastapi import APIRouter, Header, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.depends import token_verifier, get_db_session
from app.user_services import UserServices

api = APIRouter(prefix="/api", dependencies=[Depends(token_verifier)])

@api.get("/testar_login", response_class=PlainTextResponse)
def testar_login():
    return "Este endpoint só é acessível por alguém autenticado."

@api.get("/users")
def get_user(db_session: Session = Depends(get_db_session)):
    service = UserServices(db_session=db_session)
    users = service.get_users_list()
    return JSONResponse(users)

@api.get("/me", response_class=JSONResponse)
async def get_me_from_token(authorization: Optional[str] = Header(None)):
    username = UserServices.get_user_on_token(authorization);
    return {"username": username}
