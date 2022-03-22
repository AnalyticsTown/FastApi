from fastapi import FastAPI
import requests
import os
import boto3
from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

#app = FastAPI()

@app.post("/api/{mail},{password}")
def registro(mail:str, password: str):
    username =mail
    password =password

    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
    response = client.sign_up(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = username,
    Password = password
    )
    print(response)








