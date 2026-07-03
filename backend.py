from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
import uvicorn
import secrets
import json

app= FastAPI()
password_hasher=PasswordHash.recommended()


def load_users():                                               #Load or Save File
    with open("users.json", "r") as f:
        users=json.load(f)
    return users

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users,f,indent=4)

class UserCredentials(BaseModel):
    name:str=Field(min_length=3,max_length=20)
    password:str=Field(min_length=8, max_length=40)

@app.post("/auth/signup")
def signup(data:UserCredentials):
    
    users=load_users()
    for user in users:                                          #Check if name already exists
        if user["name"]==data.name:
            raise HTTPException(
                status_code=409,
                detail="Username Already Taken."
            )
    
    token=secrets.token_hex(32)
    hashed_password = password_hasher.hash(data.password)
    user_data={                                                 #Store name, hashed password, token
        "name":data.name,                                       #password_hasher.verify(data.password, stored_hash)
        "password":hashed_password,
        "token":token
    }
    users.append(user_data)                                     #store data in users.json in server
    save_users(users)

    return{
        "token":token
    }

@app.post("/auth/signin")
def signin(data:UserCredentials):
    
    users=load_users()
    for user in users:
        if user["name"]==data.name:
            if password_hasher.verify(data.password,user["password"]): #Verify password and return token
                token=user["token"]
                return{
                    "token": token
                }
            else:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect Password"
                )
    
    raise HTTPException(
        status_code= 404,
        detail="Username Not Found"
    )

@app.post("/auth/login")         #Auto Login
def autologin(authorization:str=Header()):
    return