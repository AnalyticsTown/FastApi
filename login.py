import email
from fastapi import FastAPI
import os
import boto3
#from dotenv import load_dotenv
#load_dotenv()

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

#username = 'cristianvera86@gmail.com'
#password = '&Abc1234'

@app.post("/login/{mail},{password}")
def login(mail:str,password:str):
    username= mail,
    password=password
    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
    response = client.initiate_auth(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters = {
        'USERNAME': username,
        'PASSWORD': password
    }
    )
    try:
        print (response)
        print ("logueo exitoso")
    except:
        print("algo fallo")

    at= response['AuthenticationResult']['AccessToken']
#print('RefreshToken', response['AuthenticationResult']['RefreshToken'])
