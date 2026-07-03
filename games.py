import random

def coinflip():
    pass

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