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

def high_low_call(bet,ch,comp1):
    bet_won,state,comp2=games.high_low(bet,ch,comp1)
    return bet_won,state,comp2

def slots_call(bet):
    roll,bet_amt=games.slots(bet)
    return roll,bet_amt

def show_top():
    resp=requests.get(url+"/allusers")
    state,data=check_error(resp,resp.json())
    return state,data

def start_mines_call(token,mines_number):
    body={
        "token":token,
        "mines_number":mines_number
    }
    resp=requests.post(url+"/mines/start",json=body)
    state,err=check_error(resp,resp.status_code)
    return state,err

def get_mine_data(token):
    headers={
            "authorization":token
        }
    resp=requests.post(url+"/mines/mines_pos",headers=headers)
    state,data=check_error(resp,resp.json())
    return state,data

def change_minedata(token,user_pos):
    body={
        "token":token,
        "position":user_pos
    }
    resp=requests.post(url+"/mines/update_data",json=body)
    state,err=check_error(resp,resp.status_code)
    return state,err

def delete_data(token):
    headers={
        "authorization":token
    }
    resp=requests.post(url+"/mines/delete",headers=headers)
    state,err=check_error(resp,resp.status_code)
    return state,err

def get_multiplier(mines_number,tiles_opened):
    return games.mines_multiplier(mines_number,tiles_opened)
