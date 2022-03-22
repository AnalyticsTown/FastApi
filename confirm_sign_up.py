import os
import boto3
from dotenv import load_dotenv
load_dotenv()


username = 'cristianvera86@gmail.com'
confirm_code = '869347'

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))
response = client.confirm_sign_up(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = username,
    ConfirmationCode = confirm_code
)

print(response)