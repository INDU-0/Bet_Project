import client
import random
import json
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
        print("1.Leaderboard\n2.coinflip\n3.higher lower\n4.slots\n5.mines\n6.exit")
        while True:
            try:
                choice=int(input())
                if choice==6:
                    exit()
                elif choice==1:
                    show_leaderboard()
                elif choice in [2,3,4,5]:
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
        coinflip_data(data)
    elif choice==3:
        higher_lower(data)
    elif choice==4:
        slots(data)
    elif choice==5:
        mines(data)

def coinflip_data(data):
    print(F"Current balance: {data["money"]}")
    bet_amt=enter_bet_check(data)
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

def higher_lower(data):
    print(F"Current balance: {data["money"]}")
    bet_amt=enter_bet_check(data)
    current_bal=data["money"]-bet_amt
    while True:
        print(f"current amount: {current_bal}")
        comp1=random.randint(1,16)
        print(comp1,"\n")
        print("1.Higher\n2.Lower\n3.Exit")
        try:
            choice=int(input())
            if choice==3:
                state,err=client.update_user(data["token"],current_bal+bet_amt)
                if state:
                    homepage()
                else:
                    print(err)
                    homepage()
            if choice in [1,2]:
                bet_won,won_lose,comp2=client.high_low_call(bet_amt,choice,comp1)
                print(f"The second number is {comp2}")
                if won_lose:
                    print("You Won!!")
                    current_bal+=bet_won
                    client.update_user(data["token"],current_bal)
                    homepage()
                else:
                    print("You Lost X_X")
                    current_bal-=bet_won
                    client.update_user(data["token"],current_bal)
                    homepage()
            else:
                print("enter a valid input")
        except ValueError:
            print("Enter a valid integer")

def enter_bet_check(data):
    print("Enter bet amount")
    while True:
        try:
            bet_amt=int(input())
            if data["money"]<bet_amt:
                print("Bet amt cannot exceed current balance")
            else:
                return bet_amt
        except ValueError:
            print("enter a valid integer")

def show_leaderboard():
    state,users=client.show_top()
    if state:
        users.sort(key=lambda users: users["money"], reverse=True)
        c=1
        for user in users:
            print(f"{c}.{user["name"]} -> {user["money"]}")
            c+=1
            ch=(input("Enter anything to go back to homepage"))
            if ch:
                homepage()
    else:
        print(users)
        homepage()

def slots(data):
    bet_amt=enter_bet_check(data)
    roll,bet_won=client.slots_call(bet_amt)
    print("|".join(roll))
    balance=data["money"]-bet_amt+bet_won
    print(f"New balance: {balance}")
    client.update_user(data["token"],balance)
    homepage()

def blackjack(data):
    pass

def mines(data):
    print(F"Current balance: {data["money"]}")
    print("Enter Number of mines (4-24)")
    while True:
        try:
            mines_number=int(input())
            if mines_number>24 or mines_number<4:
                print("enter a valid number between 4 and 24")
            else:
                break
        except ValueError:
            print("enter a valid integer")

    bet_amt=enter_bet_check(data)
    current_bal=data["money"]-bet_amt
    safe_tiles=25-mines_number

    state,err=client.start_mines_call(data["token"],mines_number)
    if not state:
        print(err)
        homepage()
        return

    opened=[]
    while True:
        for tile in range(1,26):
            if tile in opened:
                print(" ✓",end=" ")
            else:
                print(f"{tile:2}",end=" ")
            if tile%5==0:
                print()

        multiplier=client.get_multiplier(mines_number,len(opened))
        cashout_value=int(bet_amt*multiplier)
        print(f"Tiles opened: {len(opened)}/{safe_tiles} | Multiplier: {multiplier}x | Cash out value: {cashout_value}")
        print("Enter Tile Number (1-25) to open, or 0 to Cash Out")
        try:
            player_pos=int(input())

            if player_pos==0:
                final_balance=current_bal+cashout_value
                state,err=client.update_user(data["token"],final_balance)
                client.delete_data(data["token"])
                print(f"Cashed out!\nNew balance: {final_balance}")
                if state:
                    homepage()
                else:
                    print(err)
                    homepage()
                return

            if player_pos<1 or player_pos>25:
                print("enter a valid tile number between 1 and 25")
                continue

            if player_pos in opened:
                print("Tile already opened, choose another")
                continue

            state,mine_position=client.get_mine_data(data["token"])
            if not state:
                print(mine_position)
                homepage()
                return

            if player_pos in mine_position:
                print("💥 You hit a mine!")
                state,err=client.update_user(data["token"],current_bal)
                client.delete_data(data["token"])
                print("You Lost X_X")
                print(f"New balance: {current_bal}")
                if state:
                    homepage()
                else:
                    print(err)
                    homepage()
                return
            else:
                opened.append(player_pos)
                client.change_minedata(data["token"],player_pos)

                if len(opened)==safe_tiles:
                    multiplier=client.get_multiplier(mines_number,len(opened))
                    final_balance=current_bal+int(bet_amt*multiplier)
                    state,err=client.update_user(data["token"],final_balance)
                    client.delete_data(data["token"])
                    print("🎉 All safe tiles found! Auto cashed out!")
                    print(f"New balance: {final_balance}")
                    if state:
                        homepage()
                    else:
                        print(err)
                        homepage()
                    return
        except ValueError:
            print("enter a valid int")

def main():
    if Path("token.txt").exists():   #check if exists or not if not send to sign up or in 
        auto_login()
    else:
        choose_sign_inup()          #go to sign up or in 

if __name__=="__main__":
    main()
