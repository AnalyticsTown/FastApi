from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from decouple import config
from usuario.schemas import UsuarioRegistro, RecuperarUsuario
from dotenv import load_dotenv
import boto3

load_dotenv()


usuario = APIRouter()


"""
{
  "email": "torresfram19@gmail.com",
  "password": "#String1234"
}
"""

@usuario.post("/usuario/registro/", response_model=UsuarioRegistro, tags=['USUARIO'])
def registro(usuario: UsuarioRegistro):
    try:
        client = boto3.client(
            'cognito-idp', region_name=config('COGNITO_REGION_NAME'))

        response = client.sign_up(
            ClientId=config('COGNITO_USER_CLIENT_ID'),
            Username=usuario.email,
            Password=usuario.password,
        )

        return JSONResponse("Usuario Registrado", 200)

    except:

        return JSONResponse("No se ha podido registrar el usuario", 500)


@usuario.post("/usuario/login/", response_model=UsuarioRegistro, tags=['USUARIO'])
def login(usuario: UsuarioRegistro):

    try:
        client = boto3.client(
            'cognito-idp', region_name=config('COGNITO_REGION_NAME'))

        response = client.initiate_auth(
            ClientId=config('COGNITO_USER_CLIENT_ID'),
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': usuario.email,
                'PASSWORD': usuario.password
            }
        )

        return JSONResponse(jsonable_encoder({
            "AccessToken": response['AuthenticationResult']['AccessToken']
        }))

    except:
        return JSONResponse("No se pudo iniciar sesión", 500)


@usuario.post("/usuario/forgotpass/", tags=['USUARIO'])
def olvido_password(email: str):
    try:
        client = boto3.client(
            'cognito-idp', region_name=config('COGNITO_REGION_NAME'))

        response = client.forgot_password(
            ClientId=config('COGNITO_USER_CLIENT_ID'),
            Username=email
        )

        return JSONResponse("Email de recuperación enviado, verifique su dirección de correo", 200)

    except:
        return JSONResponse("Algo falló", 500)


@usuario.post("/usuario/forgotpassnew/", response_model=RecuperarUsuario, tags=['USUARIO'])
def confirmar_olvido_password(usuario: RecuperarUsuario):

    try:
        client = boto3.client(
            'cognito-idp', region_name=config('COGNITO_REGION_NAME')
        )

        client.confirm_forgot_password(
            ClientId=config('COGNITO_USER_CLIENT_ID'),
            Username=usuario.email,
            ConfirmationCode=usuario.codigo,
            Password=usuario.newpassword
        )

        return JSONResponse("Se ha cambiado la contraseña", 200)
    except:
        return JSONResponse("Algun error insesperado ha ocurrido", 500)
