from typing import Optional
from fastapi import APIRouter, Header, Depends, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.depends import token_verifier, get_db_session
from app.user_services import UserServices

api = APIRouter(prefix="/api", dependencies=[Depends(token_verifier)])


@api.get("/testar", response_class=JSONResponse)
def testar_login(request: Request, db_session: Session = Depends(get_db_session)):
    access_token = request.cookies.get("access_token")
    service = UserServices(db_session=db_session)
    username = service.get_user_on_token(access_token)
    return {"message": f"Este endpoint só é acessível porque {username} está autenticado."}
