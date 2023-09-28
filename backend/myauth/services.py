import environ
import os
import requests
from docops.settings import BASE_DIR

from .models import User


env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
TOKEN_REQUEST_URL=env('TOKEN_REQUEST_URL')
CLIENT_ID=env('CLIENT_ID') 
BACKEND_URL_REDIRECT=env('BACKEND_URL_REDIRECT')
CLIENT_SECRET = env('CLIENT_SECRET')

def headerFromCode(code:str)->dict:    
    request_data = {
            "client_id":CLIENT_ID,
            "client_secret":CLIENT_SECRET,
            "grant_type":"authorization_code",
            "redirect_uri" : f"{BACKEND_URL_REDIRECT}",
            "code":code
    } 
    res = requests.post(TOKEN_REQUEST_URL, data=request_data)
    res = res.json()
    try: 
        ACCESS_TOKEN=res["access_token"]
        REFRSH_TOKEN=res["refresh_token"]
        TOKEN_TYPE=res["token_type"]
        return {"Authorization" : f"{TOKEN_TYPE} {ACCESS_TOKEN}"}
    except:
        return {'res':res , "error":"some"}



def UserFromRequest(user:dict) -> list :
        username : str = user["person"]["fullName"]
        display_picture = user["person"]["displayPicture"]
        if display_picture is None:
            display_picture = 'nil' 
        roles:list = user["person"]["roles"]
        year : int = user["student"]["currentYear"]
        email : str = user["contactInformation"]["emailAddressVerified"]
        isMember : bool = False
        for role in roles:
            if role['role'] == "Maintainer" :
                isMember=True

        user , _ =User.objects.get_or_create( username=username, email=email , display_picture=display_picture, year=2)  
        print(user)

        return [user , isMember ] 
   
