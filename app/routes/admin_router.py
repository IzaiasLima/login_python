from fastapi import APIRouter, Header, Depends
from fastapi.responses import PlainTextResponse
from app.depends import admin_verifier

admin = APIRouter(prefix="/admin", dependencies=[Depends(admin_verifier)])

@admin.get("/testar_admin", response_class=PlainTextResponse)
def testar_admin():
    return "Este endpoint só é acessível por alguém com perfil ADMIN."