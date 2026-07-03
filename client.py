from pathlib import Path
import requests
from keys import url

def signup_login():
    file=Path("token.txt")

    if file.exists():
        with open("token.txt","r") as f:
            token=f.read()
        headers={                                       #automatic login 
            "Authorization":token
        }
        resp=requests.post(url+"/autologin",headers=headers)
        if resp.status_code>=400:
            print("Signin failed")
            file.unlink()
            can_exit=True
            manual_login(can_exit)

    else:
        can_exit=False
        manual_login(can_exit)
        
def manual_login(can_exit):
    if can_exit:
        choice=int(input("1.SignIn\n2.SignUp\n3.Exit"))
    else:
        choice=int(input("1.SignIn\n2.SignUp"))
    
    if choice==3:
        if can_exit:
            exit()
        else:
            print("Invalid Input")
            return
        
    body=take_input()
    if choice==1:
        endpoint="/signin"
    elif choice==2:
        endpoint="/signup"
    else:
        print("Invalid Choice")
        return
    auth(body,endpoint)

def store_token(token):
    with open("token.txt","w") as f:
        f.write(token)              #Store token

def error_checker(resp):            #check error and return token
    if resp.status_code>=400:
        print(resp.text)  
        print("Error in sign up/sign in")
        exit()
    data=resp.json()
    token=data["token"]
    return token

def take_input():                   #Take input
    name=input("Enter Username")
    password=input("Enter Password")
    body={
        "name":name,
        "password":password
    }
    return body

def auth(body,endpoint):
    resp=requests.post(url+endpoint,json=body) #signin or signup
    token=error_checker(resp)
    store_token(token) 