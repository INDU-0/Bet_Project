from pathlib import Path
from keys import url
import requests

def verify_login():
        with open ("token.txt","r") as f:
            token=f.read()
        headers={
            "authorization":token
        }
        resp=requests.post(url+"/auth/login",headers=headers)
        if resp.status_code>=400:
            Path("token.txt").unlink()
            return False
        return True

def sign_inup(name,password,endpoint):
    body={
        "name":name,
        "password":password
    }
    resp=requests.post(url+endpoint,json=body)
    if resp.status_code>=400:
        return False, resp.json()["detail"]
    return True,resp.json()["token"]

