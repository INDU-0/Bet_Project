from pathlib import Path
from keys import url
import requests
import games

def verify_login():                                 #autologin
        headers=return_header()
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
    state,data=check_error(resp,resp.json()["token"])
    return state,data
    

def get_userdata():
    headers=return_header()
    resp=requests.post(url+"/userdata",headers=headers)
    state,data=check_error(resp,resp.json())
    return state,data

    
def return_header():
    with open ("token.txt","r") as f:
        token=f.read().strip()
        headers={
            "authorization":token
        }
    return headers

def check_error(resp,rtn):
    if resp.status_code>=400:
        return False, resp.json()["detail"][0]["msg"]
    return True,rtn

def update_user(token,balance):
    body={
        "token":token,
        "balance":balance
    }
    resp=requests.post(url+"/update/userdata",json=body)
    state,err=check_error(resp,resp.status_code)
    return state,err

def coinflip_call(balance,bet,heads_tails):
    state,bal, land=games.coinflip(balance,bet,heads_tails)
    return state,bal,land