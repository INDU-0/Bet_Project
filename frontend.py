import client
from pathlib import Path

def auto_login():
    if client.verify_login():
        print("Proceeding to home..")
    else:
        choose_sign_inup()

def choose_sign_inup():
    while True:
        choice=sign_inup_menu()
        if choice==3:
            exit()
        name,password=user_input()
        if choice==1:
            endpoint="/auth/signin"
            status,token=client.sign_inup(name,password,endpoint)
        elif choice==2:
            endpoint="/auth/signup"
            status,token=client.sign_inup(name,password,endpoint)

        if status:
            store_token(token)
            print("Proceeding to home..") 
        else:
            print(token) #error msg btw

def store_token(token):
    with open("token.txt","w") as f:
        f.write(token)

def user_input():
    name=input("Enter name")
    password=input("Enter password")
    return name,password 

def sign_inup_menu():
    print("1.Signin\n2.Signup\n3.Exit")
    while True:
        try:
            choice=int(input())
            if choice in [1,2,3]:
                return choice
            else:
                print("enter a valid choice")
        except ValueError:
            print("enter a valid integer")
    
def start():
    if Path("token.txt").exists():
        auto_login()
    else:
        choose_sign_inup()
