from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from decouple import config
from dotenv import load_dotenv

from modules.usuario.models import *
from modules.usuario.schemas import *
from modules.usuario.crud import *

from modules.admin.crud import *
from modules.admin.models import *
from modules.admin.schemas import *

from db.database import get_db
from fastapi import Depends
import requests
import boto3
import json

load_dotenv()

COGNITO_REGION_NAME = config('COGNITO_REGION_NAME')
COGNITO_USER_CLIENT_ID = config('COGNITO_USER_CLIENT_ID')

usuario = APIRouter()


"""
{
  "email": "torresfram19@gmail.com",
  "password": "#String1234"
}
"""

# URLS COGNITO

url = "https://cognito-idp.{COGNITO_REGION_NAME}.amazonaws.com/".format(
    COGNITO_REGION_NAME=COGNITO_REGION_NAME)

headers = {"Content-Type": "application/x-amz-json-1.1",
           "Content-Length": "1162 // Access Token bytes length",
           "X-Amz-Target": "AWSCognitoIdentityProviderService.GetUser"}


@usuario.post("/usuario/registro/", response_model=UsuarioRegistro, tags=['USUARIO'])
def registro(usuario: UsuarioRegistro):
    try:
        client = boto3.client(
            'cognito-idp', region_name=COGNITO_REGION_NAME)

        response = client.sign_up(
            ClientId=COGNITO_USER_CLIENT_ID,
            Username=usuario.email,
            Password=usuario.password,
        )

        return JSONResponse("Usuario Registrado", 200)

    except:

        return JSONResponse("No se ha podido registrar el usuario", 500)

#INICIO DE SESION
@usuario.post("/usuario/login/", response_model=UsuarioRegistro, tags=['USUARIO'])
def login(usuario: UsuarioRegistro, db: Session = Depends(get_db)):
    # ARMAR PARA VERIFICAR SI EL USUARIO ES ADMIN O EMPLEADO
    try:
        client = boto3.client(
            'cognito-idp', region_name=COGNITO_REGION_NAME)

        response = client.initiate_auth(
            ClientId=COGNITO_USER_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': usuario.email,
                'PASSWORD': usuario.password
            }
        )

        access_token = {
            "AccessToken": response['AuthenticationResult']['AccessToken']
        }

        get_info_user = requests.post(
            url=url,
            json=access_token,
            headers=headers
        )

        aws_response = json.loads(get_info_user.text)

        admin = {
            "id_token": aws_response["UserAttributes"][0]["Value"]
        }
        create_admin(db=db, admin=admin)
        empleado = get_usuario(db=db, email=usuario.email)
        if empleado:
            return JSONResponse(jsonable_encoder(response))
        #else:
        
        
    except:
        return JSONResponse("No se pudo iniciar sesión", 500)


# OLVIDO DE CONTRASEÑA
@usuario.post("/usuario/forgotpass/", tags=['USUARIO'])
def olvido_password(email: str):
    try:
        client = boto3.client(
            'cognito-idp', region_name=COGNITO_REGION_NAME)

        response = client.forgot_password(
            ClientId=COGNITO_USER_CLIENT_ID,
            Username=email
        )

        return JSONResponse("Email de recuperación enviado, verifique su dirección de correo", 200)

    except:
        return JSONResponse("Algo falló", 500)

# REESTABLECIMIENTO DE CONTRASEÑA
@usuario.post("/usuario/forgotpassnew/", response_model=RecuperarUsuario, tags=['USUARIO'])
def confirmar_olvido_password(usuario: RecuperarUsuario):

    try:
        client = boto3.client(
            'cognito-idp', region_name=COGNITO_REGION_NAME
        )

        client.confirm_forgot_password(
            ClientId=COGNITO_USER_CLIENT_ID,
            Username=usuario.email,
            ConfirmationCode=usuario.codigo,
            Password=usuario.newpassword
        )

        return JSONResponse("Se ha cambiado la contraseña", 200)
    except:
        return JSONResponse("Algun error insesperado ha ocurrido", 500)

#CERRAR SESION
@usuario.post('/usuario/logout', tags=['USUARIO'])
def logout(access_token: str):
    try:
        client = boto3.client(
            'cognito-idp', region_name=COGNITO_REGION_NAME
        )
        response = client.logout(
            accessToken=access_token
        )
    except:
        return JSONResponse("No se pudo cerrrar sesión", 500)


# CREAR EMPLEADO
@usuario.post('/usuario/crear_empleado', tags=['USUARIO'])
def crear_empleado(usuario: UsuarioBase, db: Session = Depends(get_db)):

    try:
        client = boto3.client(
            'cognito-idp',
            region_name=COGNITO_REGION_NAME
        )

        response = client.sign_up(
            ClientId=COGNITO_USER_CLIENT_ID,
            Username=usuario.email,
            Password="#Elagronomo1234",
        )

        crear_empleado(db=db, usuario=usuario)

        return JSONResponse("Cuenta de empleado creada", 200)
    
    except:

        return JSONResponse("No se ha podido registrar el empleado", 500)
