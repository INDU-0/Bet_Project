from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
import uvicorn
import secrets
import json
import games

app= FastAPI()
password_hasher=PasswordHash.recommended()


def load_users():                                               #Load or Save File
    with open("users.json", "r") as f:
        users=json.load(f)
    return users

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users,f,indent=4)

def load_mines():                                                #Load or Save mines.json
    try:
        with open("mines.json", "r") as f:
            mines_list=json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        mines_list=[]
    return mines_list

def save_mines(mines_list):
    with open("mines.json", "w") as f:
        json.dump(mines_list,f,indent=4)

class UserCredentials(BaseModel):
    name:str=Field(min_length=3,max_length=20)
    password:str=Field(min_length=8, max_length=40)

class UpdateUser(BaseModel):
    token:str
    balance:int

class Mine_update(BaseModel):
    token:str
    position:int

class StartMines(BaseModel):
    token:str
    mines_number:int=Field(ge=4,le=24)

@app.post("/auth/signup")
def signup(data:UserCredentials):
    
    users=load_users()
    for user in users:                                          #Check if name already exists
        if user["name"]==data.name:
            raise HTTPException(
                status_code=409,
                detail=[{"msg":"Username Already Taken."}]
            )
    
    token=secrets.token_hex(32)
    hashed_password = password_hasher.hash(data.password)
    user_data={                                                 #Store name, hashed password, token, money
        "name":data.name,                                       #password_hasher.verify(data.password, stored_hash)
        "password":hashed_password,
        "token":token,
        "money":1000,
    }
    users.append(user_data)                                     #store data in users.json in server
    save_users(users)
    token={
        "token":token
    }
    return token

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
                    detail=[{"msg":"Incorrect Password"}]
                )
    
    raise HTTPException(
        status_code= 404,
        detail=[{"msg":"Username Not Found"}]
    )

@app.post("/auth/login")         #Auto Login
def autologin(authorization:str=Header()):
    return

@app.post("/userdata")
def userdata(authorization:str=Header()):
    users=load_users()
    for user in users:
        if user["token"]==authorization:
            return user
    raise HTTPException(
        status_code=404,
        detail=[{"msg":"User not found"}]
    )

@app.post("/update/userdata")
def update_userdata(data:UpdateUser):
    users=load_users()
    for user in users:
        if data.token==user["token"]:
            user["money"]=data.balance
            save_users(users)
            return
    
    raise HTTPException(
        status_code=404,
        detail=[{"msg":"Couldn't modify user"}]
    )

@app.post("/mines/start")
def start_mines(data:StartMines):
    mines_list=load_mines()
    mine_positions=games.mines(data.mines_number)                 #generate mine positions server-side

    for m in mines_list:
        if m["token"]==data.token:
            m["mine_pos"]=mine_positions
            m["opened"]=[]
            save_mines(mines_list)
            return True

    mines_list.append({
        "token":data.token,
        "mine_pos":mine_positions,
        "opened":[]
    })
    save_mines(mines_list)
    return True

@app.post("/mines/mines_pos")
def mines_pos(authorization:str=Header()):
    mines_list=load_mines()
    for user in mines_list:
        if user["token"]==authorization:
            return user['mine_pos']
    raise HTTPException(
        status_code=404,
        detail=[{"msg":"No active mines game found"}]
    )

@app.post("/mines/update_data")
def update_data(data:Mine_update):
    mines_list=load_mines()
    for user in mines_list:
        if user["token"]==data.token:
            user["opened"].append(data.position)
            save_mines(mines_list)
            return True
    raise HTTPException(
        status_code=404,
        detail=[{"msg":"User Couldnt be modified"}]
    )

@app.post("/mines/delete")
def delete_mines(authorization:str=Header()):
    mines_list=load_mines()
    for m in mines_list:
        if m["token"]==authorization:
            m["mine_pos"]=[]
            m["opened"]=[]
            save_mines(mines_list)
            return True
    raise HTTPException(status_code=404,detail=[{"msg":"User not found"}])
    

@app.get("/allusers")
def all_users():
    user=load_users()
    return user
