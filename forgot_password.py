import os
import boto3
from dotenv import load_dotenv
load_dotenv()

username = 'ssosa@moodtechnology.com.ar'

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))

response = client.forgot_password(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = username
)

print(response)