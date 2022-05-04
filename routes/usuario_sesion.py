from fastapi import APIRouter
# import requests

import os
import boto3
from usuario.schemas import UsuarioRegistro, RecuperarUsuario

from dotenv import load_dotenv
load_dotenv()


usuario = APIRouter()


@usuario.post("/usuario/registro/", response_model=UsuarioRegistro, tags=['USUARIO'])
async def registro(usuario: UsuarioRegistro):
    print(usuario)
    try:
        client = await boto3.client(
            'cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
        response =  await client.sign_up(
            ClientId= os.getenv('COGNITO_USER_CLIENT_ID'),
            Username= usuario.email,
            Password= usuario.password,
        )
        print(response)    
    except:
        return 'error'
    
    

@usuario.post("/usuario/login/", response_model=UsuarioRegistro, tags=['USUARIO'])
async def login(usuario: UsuarioRegistro):

    try:
        client= await boto3.client(
            'cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
        response= await client.initiate_auth(
            ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': usuario.email,
                'PASSWORD': usuario.password
            }
        )
        print(response)
        # at = response['AuthenticationResult']['AccessToken']
        # return {"message": "logueo exitoso"}
    except:
        return {"message": "algo falló"}


@ usuario.post("/usuario/forgotpass/", tags=['USUARIO'])
async def olvido_password(email: str):
    try:
        client= await boto3.client(
            'cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))

        response= await client.forgot_password(
            ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
            Username=email
        )

        return(response)
        # return("se ha enviado su correo")

    except:
        return "algo falló"


@ usuario.post("/usuario/forgotpassnew/", response_model=RecuperarUsuario, tags=['USUARIO'])
async def confirmar_olvido_password(usuario: RecuperarUsuario):

    try:
        client= await boto3.client(
            'cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME')
        )
        response= await client.confirm_forgot_password(
            ClientId=os.getenv('COGNITO_USER_CLIENT_ID'),
            Username=usuario.email,
            ConfirmationCode=usuario.codigo,
            Password=usuario.newpassword
        )

        print(response)
        return "se ha cambiado la contraseña"
    except:
        return "algo falló"
