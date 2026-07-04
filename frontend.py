import client
from pathlib import Path

def auto_login():
    if client.verify_login():           #verify login if not then false is returned and it goes to sign up or in
        print("Proceeding to home..")
        homepage()
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
            status,token=client.sign_inup(name,password,endpoint)       #sign in 
        elif choice==2:
            endpoint="/auth/signup"
            status,token=client.sign_inup(name,password,endpoint)       #sign up

        if status:                                                      #if no error then store token, if error print error and repeat
            store_token(token)
            print("Proceeding to home..") 
            homepage()
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

def homepage():
    state,data=client.get_userdata()                                                #take data             
    if state:
        balance=data["money"]                                                       #show homepage and take input
        print(f"Welcome To Degenerate's Cave")
        print(f"Balance: {balance}")
        print("1.Leaderboard\n2.blackjack\n3.coinflip\n4.higher lower\n5.slots\n6.mines\n7.exit")
        while True:
            try:
                choice=int(input())
                if choice==7:
                    exit()
                elif choice==1:
                    show_leaderboard()
                elif choice in [2,3,4,5,6]:
                    games(choice,data)
                else:
                    print("Enter a valid choice")
            except ValueError:
                print("enter a valid integer")
    else :
        print(data)
        choose_sign_inup()

def games(choice,data):   #didnt add the update data part yet and then the show the output of teh thingy yet 
    if choice==2:
        pass
    elif choice==3:
        coinflip_data(data)

def coinflip_data(data):
    print(F"Current balance: {data["money"]}")
    print("Enter bet amount")
    bet_amt=0
    while True:
        try:
            bet_amt=int(input())
            if data["money"]<bet_amt:
                print("Bet amt cannot exceed current balance")
            else:
                break
        except ValueError:
            print("enter a valid integer")
    print("1.Heads\n2.Tails")
    while True:
        try:
            hd_tl=int(input())
            if hd_tl in [1,2]:
                state,balance,land=client.coinflip_call(data["money"],bet_amt,hd_tl)
                if land==1:
                    print("The coin landed on Heads")
                if land==2:
                    print("The coin laned on Tails")
                
                if state:
                    print("You Won!!")
                    print(f"New balance: {balance}")
                else:
                    print("You Lost X_X")
                    print(f"New balance: {balance}")
                
                state,err=client.update_user(data["token"],balance)
                if state:
                    homepage()
                else:
                    print(err)
                    homepage()
                    
            else:
                print("enter a valid choice")
        except ValueError:
            print("enter a valid integer")

def show_leaderboard():
    pass

def start():
    if Path("token.txt").exists():   #check if exists or not if not send to sign up or in 
        auto_login()
    else:
        choose_sign_inup()          #go to sign up or in 

if __name__=="__main__":
    start()