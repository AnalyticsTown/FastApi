import os
import boto3
from dotenv import load_dotenv
load_dotenv()

username = 'ssosa@moodtechnology.com.ar'
confirm_code = '996486'
new_password = '#1234Abc'

client = boto3.client('cognito-idp', region_name=os.getenv('COGNITO_REGION_NAME'))

response = client.confirm_forgot_password(
    ClientId = os.getenv('COGNITO_USER_CLIENT_ID'),
    Username = username,
    ConfirmationCode = confirm_code,
    Password = new_password

)

print(response)