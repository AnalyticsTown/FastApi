from fastapi import ApiRouter
#import requests
import os
import boto3
#from dotenv import load_dotenv
#load_dotenv()
from fastapi.middleware.cors import CORSMiddleware

usuario = ApiRouter()

@usuario.post("/registro/{mail},{password}")
def registro(mail:str, password: str):
    #username =mail
    #password =password

    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
    response = client.sign_up(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = mail,
    Password = password
    )
    print(response)
    
@usuario.post("/login/{mail},{password}")
def login(mail:str, password:str):
   
    #username= mail,
    #contrasenia=password
    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
    response = client.initiate_auth(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    AuthFlow ='USER_PASSWORD_AUTH',
    AuthParameters = {
        'USERNAME': mail,
        'PASSWORD': password
    }
    )
   
    try:
        return (response)
        at= response['AuthenticationResult']['AccessToken']
        return {"message": "logueo exitoso"}
    except:
        return {"message": "algo falló"}

@usuario.post("/forgotpass/{mail}")
def olvidoPass(mail:str):
    
    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))

    response = client.forgot_password(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = mail
)
    try:
        return(response)
        return("se ha enviado su correo")
        
    except:
        return("algo falló")

@usuario.post("/forgotpassnew/{mail},{codigo},{newpass}")
def confirmaolivopass(mail:str,codigo:str,newpass:str):
    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))

    response = client.confirm_forgot_password(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = mail,
    ConfirmationCode = codigo,
    Password = newpass

    )
    try:
        print(response)
        return("se ha cambiado la contraseña")
    except:
        return("algo falló")
