from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from app.routes.api_router import api
from app.routes.user_router import user
from app.routes.admin_router import admin

app = FastAPI(
    title="Cadastro de Prestadores de Serviços",
    version="0.0.1",
    description="Protótipo de uma API para gerir um cadastro de prestadores de serviços freelancers. ",
)

app.include_router(admin)
app.include_router(user)
app.include_router(api)

@app.get("/", response_class=PlainTextResponse)
def get_info():
    return f"{app.title}, versão {app.version}\nDescrição: {app.description}" 

@app.get("/aberto", response_class=PlainTextResponse)
def rota_aberta():
    return "Este endpoint é aberto para acesso público"
