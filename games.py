import random

def coinflip(balance,bet,user_ht:int): #balance is bet minus balance
    head_tail=random.randint(1,3) #1 is head, 2 is tails
    balance=balance-bet
    if head_tail==user_ht:
        balance=int(balance+(bet*(1.5)))
        return True,balance,head_tail
    else:
        return False, balance, head_tail

def blackjack():
    deck = []
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank}{suit}")
    random.shuffle(deck)

    dealer_hand=[]
    player_hand=[]
    for r in range(2):
        dealer_hand.append(deck.pop())
        player_hand.append(deck.pop())

    #we gotta show dealer 1 and give the player both of his cards
    

def high_low():
    pass

def slots():
    pass

def mines():
    pass