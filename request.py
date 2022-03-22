import requests
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

#parametros = {'clave1': 'valor1', 'clave2': ['val1', 'val2']}
r= requests.post('/login.js')
posts = r.json()
parametros={'user':'Usuario', 'password':'password'}


def logueo(parametros):
    username = parametros[0]
    password = parametros[1]

    client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
    response = client.sign_up(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = username,
    Password = password
    )
    print(response)

logueo()
