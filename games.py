import random

def coinflip(balance,bet,user_ht:int): #balance is bet minus balance
    head_tail=random.randint(1,3) #1 is head, 2 is tails
    balance=balance-bet
    if head_tail==user_ht:
        balance=int(balance+(bet*(1.5)))
        return True,balance,head_tail
    else:
        return False, balance, head_tail
    
def high_low(bet,ch,comp1):
    low = max(1, comp1 - 3)
    high = min(15, comp1 + 3)
    comp2=random.randint(low,high)

    if comp1==comp2:
        bet=bet*10
        state=True
    if ch==1 and comp1<comp2:
        bet=bet*(comp2-comp1)
        state=True
    elif ch==1 and comp1>comp2:
        bet=bet*(comp2-comp1)
        state=False
    elif ch==2 and comp1>comp2:
        bet=bet*(comp1-comp2)
        state=True
    elif ch==2 and comp1<comp2:
        bet=bet*(comp2-comp1)
        state=False

    return bet,state,comp2

def slots(bet):
    symbols=["🍒","🍒","🍒"
            ,"🍋","🍋","🍋",
            "🍊","🍊","🍊",
            "🔔","🔔","🔔",
            "💎","💎","💎"]
    roll = random.choices(symbols, k=3)
    
    if roll[0] == roll[1] == roll[2]:
        return roll,(bet*3)
    elif len(set(roll)) == 2:
        return roll,int(bet*2)
    else:
        return roll,(bet*0)

def mines(mines_number):
    positions=random.sample(range(1,26),mines_number)
    return positions

def mines_multiplier(mines_number,tiles_opened,house_edge=0.97):
    total_tiles=25
    fair_multiplier=1.0
    for i in range(tiles_opened):
        fair_multiplier*=(total_tiles-i)/(total_tiles-mines_number-i)
    multiplier=1+(fair_multiplier-1)*house_edge
    return round(multiplier,2)


'''
{token:
mine_pos:
opened:
}'''
