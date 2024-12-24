from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.depends import token_verifier, get_db_session, get_body
from app.user_services import UserServices
from app.member_services import MemberServices

api = APIRouter(prefix="/api", dependencies=[Depends(token_verifier)])

@api.post("/members/add")
def member_register(request:Request, form_member = Depends(get_body),
    db_session: Session = Depends(get_db_session),
):
    print(len(form_member))
    access_token = request.cookies.get("access_token")
    user_service = UserServices(db_session=db_session)
    user = user_service.get_user_on_token(access_token)

    member_service = MemberServices(db_session=db_session)
    member_service.member_register(user, form_member)

    return JSONResponse(
        content={"message": "New member added."}, status_code=status.HTTP_201_CREATED
    )


@api.get("/user_name", response_class=PlainTextResponse)
def get_user_name(request: Request, db_session: Session = Depends(get_db_session)):
    access_token = request.cookies.get("access_token")
    service = UserServices(db_session=db_session)
    username = service.get_user_on_token(access_token)
    return username
