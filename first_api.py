from fastapi import FastAPI
#import requests
import os
import boto3
#from dotenv import load_dotenv
#load_dotenv()
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

#app = FastAPI()

@app.post("/registro/{mail},{password}")
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
    
@app.post("/login/{mail},{password}")
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
        print (response)
        at= response['AuthenticationResult']['AccessToken']
        return {"message": "logueo exitoso"}
    except:
        return {"message": "algo falló"}





