# !/usr/bin/env python3
# 

# Author: Matthew Ryan LaGreca
# still to implement: adding new lines where appropriate to make the game run more appropriately, Basic Strategy,
# putting things in their own functions/classes/modules, gamepy it, card counter tracker, a timer to track session length
# Lucky Ladies side bet (along with pay table explanation), clean up the hand display functionality

from random import shuffle, randint
from datetime import timedelta, date
from time import sleep

class Card():
    '''The class for an individual playing card'''

    # All of the potential point values a card can hold in BlackJack
    POINT_VALUES = {

        # Each card is worth a static amount of points, besides an Ace
        'Ace' : 11, # Ace can either count as a 1 or an 11, for now we are handling this in another method in the Player class called "hand_total"
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9,
        '10' : 10,
        'Jack' : 10,
        'Queen' : 10,
        'King' : 10

    }

    # A standard playing card can have 1 of 4 suits
    SUITS = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

    def __init__(self, value, suit):
        self.value = value

        # making sure that during the initialization of each card that the point value is also stored in the card
        self.points = self.POINT_VALUES[value]
        self.suit = suit
    
    def __repr__(self):
        return f'{self.value} of {self.suit}'

class Cut_Card(Card):
    """# A special card of no value, usually just a solid color fill, 
    when it comes out of the shoe signals to the dealer to shuffle once that round of play has ended"""

    def __init__(self):
        self.value = 0
        self.points = 0
        self.suit = None
        self.color = 'Yellow' # Color doesn't matter here, just adding it to further distinguish the cut card from a standard one
    
    def __repr__(self):
        return f'A {self.color} card with {self.value} value and {self.suit} suit; signals to the dealer to shuffle once the current round of play has ended'

class Deck():
    '''This class when instantiated will generate a standard deck of playing cards
    It will also automatically shuffle them for us'''

    def __init__(self):
        self.cards = []
        self.generate_deck()
        self.shuffle_deck()

    # This will automatically generate a deck of 52 cards
    def generate_deck(self):
        for value in Card.POINT_VALUES:
            for suit in Card.SUITS:
                self.cards.append(Card(value,suit))
    
    # This will shuffle the deck; just realized that I probably could have just called shuffle(self.cards) and called it a day on this one lol
    def shuffle_deck(self):

        # # Creates an array with indices from 0-51
        # order = [i for i in range(52)]

        # # Shuffles the list for us
        # shuffle(order)

        # # Using list comprehension, we generate another list to create tuples
        # # each tuple contains the new order and the card to be shuffled into that order
        # cards_to_shuffle = [(order[i],self.cards[i]) for i in range(52)]

        # # sorting completes the shuffle of the cards
        # cards_to_shuffle.sort()

        # # sets the newly shuffled deck to self.cards
        # self.cards = [cards_to_shuffle[i][1] for i in range(52)]

        # Trying using just shuffle(self.cards) lol
        shuffle(self.cards)

class Shoe():
    '''This class when instantiated will generate a shoe of X decks of playing cards
    It will also automatically shuffle it for us'''

    # instantiating a cut card to be inserted randomly in the shoe
    shuffle_card = Cut_Card()

    def __init__(self,size):
        self.size = size
        self.num_cards = size*52 # This is currently a redundant variable
        self.cards = []
        self.generate_shoe()
        self.shuffle_shoe()

    def generate_shoe(self):
        for i in range(self.size):
            for card in Deck().cards:
                self.cards.append(card)

    def shuffle_shoe(self):

        # a display message for the user
        print('Shuffling cards...')
        sleep(.8)

        # # Lol, I did it here too
        # order = [i for i in range(self.num_cards)]
        # shuffle(order)
        # cards_to_shuffle = [(order[i],self.cards[i]) for i in range(self.num_cards)]
        # cards_to_shuffle.sort()
        # self.cards = [cards_to_shuffle[i][1] for i in range(self.num_cards)]
        shuffle(self.cards)
        self.cards.insert(randint(25,51),self.shuffle_card)
        # self.cards.append(self.shuffle_card)
    
    # the function to deal an individual card to the designated player
    def deal(self):
        return self.cards.pop(-1)
    
    # a function to check and see if the cut card has come out
    def check_cut_card(self):
        if self.cards[-1] == self.shuffle_card:
            print('The cut card has come out; this is the last round of play before the shuffle')
            sleep(.8)
            self.cards.pop(-1)
            return True
        
    # this allows us to insert cards back into the shoe, typically from the discard tray  
    def insert_cards(self, cards):
        while cards:
            shoe.cards.append(cards.pop())
        
class DiscardTray():
    """The discard tray is where we discard cards after each round of play,
    so that they can be reused when it's time to shuffle"""

    def __init__(self):
        self.name = 'discard_tray'
        self.cards = []

    # inserting cards into the discard tray
    def insert_card(self, discarded_card):
            self.cards.append(discarded_card)
    
    # taking all the cards out of the discard tray and putting them back in the shoe
    # this function actually never made it into the code
    def empty_tray(self, shoe):
        for discarded_card in self.cards:
            shoe.cards.append(discarded_card)
    
    def __repr__(self):
        return f'{self.cards}'

class Player():
    """A class for each generic player"""

    def __init__(self, name):
        self.name = name
        self.bankroll = 0 #aka, the money the player came to play with
        self.winnings = 0 # total amount won or lost after leaving the game
        self.hands = [[],[],[],[]] # a player can split their hand when appropriate, up to 4 times
        self.current_hand = self.hands[0] # keeping track of which hand is currently being acted on
        self.hand_total = 0 # the total for the current hand (? may not actually be true)
        self.hand_totals = [0,0,0,0] # the total for each hand
        self.wagers = [0,0,0,0] # the amount of money riding on each hand 
        self.current_wager = self.wagers[0] # the amount of money riding on the current hand being acted on

    # dealing the player a card, and then updating the total for the hand
    def assign_card(self, card):
        self.current_hand.append(card)
        self.total_of_cards()
    
    # showing the hand 
    def show_hand(self):
        print(f"Your current hand: {self.current_hand}")
        sleep(.8)
        if self.current_hand == Cut_Card():
            print("The cut card has come out; this is the last round before the shuffle")
            sleep(.8)
            return self.current_hand.pop(-1)

    # registering how much money the player has available to use for blackjack
    def assign_bankroll(self,bankroll):
        if bankroll > 0:
            self.bankroll = bankroll
        else:
            print("You cannot have a bankroll less than $1")

    # keeping track of the outcomes of each hand, in terms of how it affects the bankroll and the winnings
    def update_bankroll(self, change):
        self.bankroll += change
        self.winnings += change

    # we need to know how much we are initially putting up for the hand at the start of each round of play
    def initial_wager(self, table_min, table_limit):
        while True:
            try:
                bet = float(input(f'How much would you like to bet? You currently have ${self.bankroll} $'))
                if bet < table_min:
                    sleep(.8)
                    print(f'You cannot place a bet less than the table minimum of ${table_min}')
                elif bet > table_limit:
                    sleep(.8)
                    print(f'You cannot bet more than the table limit of ${table_limit}')
                elif bet > player1.bankroll:
                    sleep(.8)
                    print(f'You cannot exceed your bankroll: you have ${player1.bankroll}; you tried to place a bet of ${bet}')
                else:
                    sleep(.8)
                    print(f'A bet of ${bet} has been placed; good luck to you')
                    return bet
            except:
                sleep(.8)
                print('You did not input a valid wager; please try again')

    # this function keeps track of the increases in the bet on the current hand in play
    def increase_hand_wager(self, wager):
        index = self.wagers.index(self.current_wager)
        self.wagers[index] += wager
        self.current_wager = self.wagers[index]

    # Oh boy, the function that is breaking everything but is seemingly working, the hand splitting function
    # A place to check first to see where the edge case is occurring
    def hand_split(self, current_hand, wager):
        if len(current_hand) > 2:
            sleep(.8)
            print('You can not split a hand larger than 2 cards')
            return 0
        elif [] not in self.hands:
            sleep(.8)
            print('You have already split to the maximum of 4 hands')
            return 0
        elif current_hand[0].points != current_hand[1].points:
            sleep(.8)
            print(f'You can not split {current_hand[0].value}, {current_hand[1].value}')
            return 0
        index = self.hands.index(current_hand)
        for i in range(index,len(self.hands)-1):
            if self.hands[i+1] == []:
                self.hands[i+1].append(self.hands[index].pop(-1))
                sleep(.8)
                print(f'You put up the additional ${wager} for the split')
                self.wagers[i+1] += wager
                break
        self.show_of_hands()
        return wager

    # this function shows all the hands the player has made or not made if empty
    # needs to be reformatted to be cleaner and not show empty hand
    def show_of_hands(self):
        sleep(.8)
        print(f'Your hands are: {self.hands}')

    # discards the cards into the discard tray and sets everything back to 0 for the wagers           
    def discard_hand(self, discard_tray):
        for hand in self.hands:
            while hand:
                discard_tray.insert_card(hand.pop())
        self.wagers = [0,0,0,0]
        self.current_wager = self.wagers[0]
    
    # creates a total of all the cards to be checked when showdown happens
    def total_of_cards(self):

        sum = 0
        card_values = [card.value for card in self.current_hand]
        for card in self.current_hand:
            sum += card.points
        
        # this section of code prevents the "Bust" status from happening prematurely
        # we want to make sure that soft totals are accurately converted to hard totals
        if sum > 21 and 'Ace' in card_values:
            ace_count =  card_values.count('Ace')
            while sum > 21 and ace_count > 0:
                sum -= 10
                ace_count -=1

        # an old debugging print statement
        # print(sum)
        self.hand_total = sum

    # we need to see if the status of the current (?, this also might not be correct) hand is busted or not
    def status(self):

        if self.hand_total > 21:
            return 'Bust'
        else:
            return 'Good'
    
    # when called, this is supposed to change which hand is the current hand
    def change_hands(self):
        if self.current_hand == self.hands[0]:
            self.current_hand = self.hands[1]
            self.current_wager = self.wagers[1]
        elif self.current_hand == self.hands[1]:
            self.current_hand = self.hands[2]
            self.current_wager = self.wagers[2]
        elif self.current_hand == self.hands[2]:
            self.current_hand = self.hands[3]
            self.current_wager = self.wagers[3]
        else:
            self.current_hand = self.hands[0]
            self.current_wager = self.wagers[0]

class Dealer(Player):
    """As a subclass of the generic player class,
    they always act last in a round of play and they hide
    one of their cards so as to cause distress to the players
    and also add to the mathematical house edge over the players"""

    def __init__(self):
        super().__init__('Dealer')
    
    # this function makes it so we hide the hole card when we call for the
    # the dealer's hand to be shown pre showdown
    def show_hand(self):
        if len(self.current_hand) == 1:
            print(f"Dealer's Hand: ['hidden']")
            sleep(.8)
        elif len(self.current_hand) == 2:
            print(f"Dealer's Hand: ['hidden', {self.current_hand[1]}]")
            sleep(.8)
        else:
            print(f"Dealer's Hand: {self.current_hand}")
            sleep(.8)
    
    # showing the actual hand during showdown
    def show_actual_hand(self):
        print(f"Dealer's Hand: {self.current_hand}")
        sleep(.8)

# a simple class that will tell you what to do with a specific hand against a dealer's up card (WIP)
class Basic_Strategy():

    # pair_splitting = {
    #     [11,11] : 'Always Split',
    #     [10,10] : 'Never Split',
    #     [9,9] : 'Against 2 through 6, 8 and 9: Split',
    #     [8,8] : 'Always Split',
    #     [7,7] : 'Against 2 through 7: Split',
    #     [6,6] : 'Against 2 through 6: Split',
    #     [5,5] : 'Never Split',
    #     [4,4] : 'Against 5 and 6: Split',
    #     [3,3] : 'Against 2 through 6: Split',
    #     [2,2] : 'Against 2 through 6: Split'
    # }

    soft_totals = {
        20: 'Stand',
        19: 'Double against a 6 if you can, otherwise Stand',
        18: 'Double against a 2 through 6 if you can, otherwise Stand; if Dealer has 9, 10/Face, or Ace: Hit; stand on Dealer 7 and 8',
        17: 'Double against a 3 through 6 if you can, otherwise Hit; if Dealer has 2, 7 or higher: Hit',
        16: 'Double against a 4 through 6 if you can, otherwise Hit; if Dealer has 2, 3, 7 or higher: Hit',
        15: 'Double against a 4 through 6 if you can, otherwise Hit; if Dealer has 2, 3, 7 or higher: Hit',
        14: 'Double against a 5 or 6 if you can, otherwise Hit; if Dealer has 2 through 4, 7 or higher: Hit',
        13: 'Double against a 5 or 6 if you can, otherwise Hit; if Dealer has 2 through 4, 7 or higher: Hit',
    }

    hard_totals = {
        20: 'Stand',
        19: 'Stand',
        18: 'Stand',
        17: 'Stand',
        16: 'Stand on Dealer 2 through 6, Hit on 7+',
        15: 'Stand on Dealer 2 through 6, Hit on 7+', 
        14: 'Stand on Dealer 2 through 6, Hit on 7+', 
        13: 'Stand on Dealer 2 through 6, Hit on 7+', 
        12: 'Stand on Dealer 4 through 6, Hit on 2, 3, and 7+',
        11: 'Double if you can, otherwise hit',
        10: 'Double if you can against 9 and below, otherwise hit; hit against 10/Face and Ace',
        9: 'Double if you can against 3 through 6, otherwise hit; hit against 2 and 7 or higher',
        8: 'Hit',
        7: 'Hit',
        6: 'Hit',
        5: 'Hit',
        4: 'Hit',
    }

    def bs(player_cards, dealer_upcard):
        pass

def deal_starting_cards():
    """This function deals out the initial cards for the players,
    while making sure to check for the cut card before each card is
    dealt to the player"""

    cut_card = False
    if(shoe.check_cut_card()):
        cut_card = True
    player1.assign_card(shoe.deal())
    player1.show_hand()
    sleep(.8)
    if(shoe.check_cut_card()):
        cut_card = True
    player2.assign_card(shoe.deal())
    player2.show_hand()
    sleep(.8)
    if(shoe.check_cut_card()):
        cut_card = True
    player1.assign_card(shoe.deal())
    player1.show_hand()
    sleep(.8)
    if(shoe.check_cut_card()):
        cut_card = True
    player2.assign_card(shoe.deal())
    player2.show_hand()
    sleep(.8)
    if cut_card:
        return cut_card

# deck1 = Deck()
# print(deck1.cards)
# print(len(deck1.cards))
# deck1.shuffle_deck()
# deck1.shuffle_deck()

# card = Cut_Card()
# print(card)


#Opening sequence
name = input('Welcome to BlackJack!  What is your name? ')
player1 = Player(name)
print(f'Nice to meet you, {name}')
sleep(.8)
table_min = 5
table_limit = 1000
print(f'The table minimum is ${table_min} and the table limit is ${table_limit}')
sleep(.8)
while True:
    try:
        bankroll = int(input("How much money did you bring with you to play today? $"))
        if bankroll >= table_min:
            player1.assign_bankroll(bankroll)
            break
        else: 
            print(f'Please input least the table min of ${table_min} for your money')
            sleep(.8)
    except:
        print('Please input a valid integer for your money')
        sleep(.8)
print(f'Awesome; cashing in ${bankroll}')
sleep(.8)
player2 = Dealer()    
deck_count = 0
while True:
    try:
        deck_count = int(input("How many decks do you want to play with today? You can choose an integer between 1 and 8: "))
        if player1.bankroll >= 1:
            break
    except:
        print('Please input a valid integer for the number of decks you want to play with')
        sleep(.8)   
shoe = Shoe(deck_count)
discard_tray = DiscardTray()
cut_card = False
#Gameplay loop, not having accounted for shuffling
while True:
    wager = player1.initial_wager(table_min,table_limit)
    player1.increase_hand_wager(wager)
    total_wagered = wager
    player1.current_hand = player1.hands[0]
    # print(player1.current_wager)
    # print(player1.wagers[0])
    sleep(.8)
    if deal_starting_cards():
        cut_card = True
    
    #Testing blackjack case
    # player1.assign_card(Card('Ace','Spades'))
    # player1.assign_card(Card('King','Spades'))
    # player2.assign_card(Card('King','Spades'))
    # player2.assign_card(Card('King','Spades'))

    # testing split
    # player1.assign_card(Card('Ace','Spades'))
    # player1.assign_card(Card('Ace','Spades'))
    # player2.assign_card(Card('9','Spades'))
    # player2.assign_card(Card('5','Spades'))
    choice = ''

    #Setting some flags
    surrender = False
    blackjack = False
    dealer_blackjack = False
    initial_deal_1 = True
    initial_deal_2 = True


    if player1.hand_total == 21:
        blackjack = True
    if player2.hand_total == 21:
        dealer_blackjack = True

    for hand in player1.hands:
            # This first part is handling every blackjack (player or dealer) scenario, including insurance
        if initial_deal_1:

            # If you get Blackjack and the dealer doesn't have blackjack
            if blackjack and not dealer_blackjack:
                wager *=1.5
                print(f'BLACKJACK!  You win ${wager}')
                sleep(.8)
                player1.update_bankroll(wager)
                player2.show_actual_hand()
                break

            #If you get Blackjack and the dealer is showing an Ace
            elif blackjack and player2.current_hand[1].value == 'Ace':
                while True:
                    even_money = input('Would you like Even Money? (y/n) ').strip().lower()
                    if even_money in {'yes', 'ye', 'y', 'n', 'no', 'nah'}:
                        break
                    else:
                        print(f'{even_money} is an invalid response; please try again')
                        sleep(.8)
                if even_money in {'n', 'no', 'nah'}:
                    if dealer_blackjack:
                        player2.show_actual_hand()
                        print("Dealer has Blackjack: you push")
                        break
                    else:
                        wager *=1.5
                        print(f'BLACKJACK!  You win ${wager}')
                        sleep(.8)
                        player1.update_bankroll(wager)
                        player2.show_actual_hand()
                        break
                else:
                    print(f'Taking even money: you win ${wager}')
                    sleep(.8)
                    player1.update_bankroll(wager)
                    player2.show_actual_hand()
                    break
            
            #Handling insurance
            elif player2.current_hand[1].value == 'Ace':
                while True:
                    insurance = input('Would you like insurance? (y/n) ').strip().lower()
                    if insurance in {'yes', 'ye', 'y', 'n', 'no', 'nah'}:
                        break
                    else:
                        print(f'{insurance} is an invalid response; please try again')
                        sleep(.8)
                if insurance in {'n', 'no', 'nah'} or player1.bankroll - wager*1.5 < 0:
                    if player1.bankroll - wager*1.5 < 0:
                        print("You don't have enough money for the insurance bet")
                        sleep(.8)
                    if dealer_blackjack:
                        player2.show_actual_hand()
                        print(f"Dealer has Blackjack: you lose ${wager}")
                        sleep(.8)
                        player1.update_bankroll(-wager)
                        break
                    else:
                        print("Nobody's home")
                        sleep(.8)
                        
                else:
                    print(f"You put up ${wager/2} for insurance")
                    sleep(.8)
                    if dealer_blackjack:
                        player2.show_actual_hand()
                        print(f"Dealer has Blackjack; nice call")
                        sleep(.8)
                        break
                    else:
                        print(f"Nobody's home: you lose your insurance bet of ${wager/2}")
                        sleep(.8)
                        player1.update_bankroll(-wager/2)
                        

            #Handling Dealer Blackjack with 10 showing instead of ace:
            elif dealer_blackjack:
                if blackjack:
                    player2.show_actual_hand()
                    print("Dealer has Blackjack: you push")
                    sleep(.8)
                    break
                else:
                    player2.show_actual_hand()
                    print(f"Dealer has Blackjack: you lose ${wager}")
                    sleep(.8)
                    player1.update_bankroll(-wager)
                    break
            elif not dealer_blackjack and player2.current_hand[1].points == 10:
                print("Nobody's Home")
                sleep(.8)
            initial_deal_1 = False # making sure that this sequence can't be checked for every hand
    
        if hand == []: #if the hand doesn't exist, we don't want to play with it
            continue
        elif len(hand) == 1: # if the hand was split, we automatically deal 1 card to it
            if(shoe.check_cut_card()):
                cut_card = True
            player1.assign_card(shoe.deal())
            # player1.assign_card(Card('Ace','Clubs'))
        player1.show_hand()
        player2.show_hand()

        # allow this gameplay to keep happening until the player busts or breaks out with a stand or double down
        while player1.status() != 'Bust':
            if len(hand) == 1: # if the hand was split, we automatically deal 1 card to it
                if(shoe.check_cut_card()):
                    cut_card = True
                player1.assign_card(shoe.deal())
                # player1.assign_card(Card('Ace','Clubs')) an old test case
                player1.show_hand()
            choice = input(f'What would you like to do? Your hand total is {player1.hand_total}\n Hit (h), Stand (s), Surrender (u), Split (p) or Double Down (dd) ').lower().strip()

            if choice in {'hit', 'h'}:
                if(shoe.check_cut_card()):
                    cut_card = True
                player1.assign_card(shoe.deal())
            elif choice in {'stand','st', 's'}:
                print(f'{player1.name} stands with {player1.hand_total}')
                sleep(.8)
                break
            elif choice in {'surrender','su', 'u'}:

                # we only want to be able to surrender if the hand we are playing on are the original 2 cards dealt to the player
                if len(player1.current_hand) == 2 and initial_deal_2: 
                    wager /= 2
                    print(f"You have chosen to surrender; here is ${wager} back")
                    sleep(.8)
                    player1.update_bankroll(-wager)
                    surrender = True
                    initial_deal_2 = False
                    player2.show_actual_hand()
                    break
                else:
                    print('You cannot surrender after you have played on your initial two cards')
                    sleep(.8)
            elif choice in {'split','sp', 'p'}:
                if total_wagered + wager > player1.bankroll:
                    print(f"You don't have the additional ${wager} in your bankroll to split; you currently have ${player1.bankroll - total_wagered} left")
                    sleep(.8)
                else:
                    # player1.hand_split(player1.current_hand, wager)
                    total_wagered += player1.hand_split(player1.current_hand, wager)
            elif choice in {'double down', 'double', 'dd'}: #This needs to be fixed for the case where the bankroll is less than the wager
                if len(player1.current_hand) == 2 :
                    try: 
                        doubling_for = float(input(f"How much would you like to double down for? You can double down between $1 and ${wager}: $"))
                        if total_wagered + doubling_for > player1.bankroll:
                            print(f"You don't have the additional ${doubling_for} in your bankroll to double down; you currently have ${player1.bankroll - total_wagered} left")
                            sleep(.8)
                        elif doubling_for < wager and doubling_for >= 1:
                            print(f"Doubling for less with ${doubling_for}")
                            sleep(.8)
                            if(shoe.check_cut_card()):
                                cut_card = True
                            player1.assign_card(shoe.deal())
                            player1.increase_hand_wager(doubling_for)
                            total_wagered += doubling_for
                            break
                        elif doubling_for == wager:
                            print(f'Doubling down: you put up ${wager} for the Double Down')
                            sleep(.8)
                            if(shoe.check_cut_card()):
                                cut_card = True
                            player1.assign_card(shoe.deal())
                            player1.increase_hand_wager(wager)
                            total_wagered += wager
                            break
                        else:
                            print(f'${doubling_for} is not a valid amount to Double Down')
                            sleep(.8)
                    except:
                        print(f'{doubling_for} is not a valid input; you can double down between $1 and ${wager}')
                        sleep(.8)
                else:
                    print('You have more than 2 cards in your hand; you cannot Double Down')
                    sleep(.8)
            else:
                print(f'{choice} is not a valid selection, please try again')
            initial_deal = False
            player1.show_hand()
            player2.show_hand()
        player1.change_hands()
        player1.show_of_hands()

    #After player play decision matrix
    player1.current_wager = player1.wagers[0]
    player1.current_hand = player1.hands[0]
    if not blackjack and not dealer_blackjack and not surrender:
        print(f'Play will now go to the dealer')
        sleep(.8)
    for hand in player1.hands:
        if blackjack or dealer_blackjack:
            continue
        elif surrender:
            continue
        if hand == []:
            player1.change_hands()
            continue
        player1.total_of_cards()
        player1.show_hand()
        if player1.status() != 'Bust':
            while player2.status() != 'Bust':
                player2.show_actual_hand()
                print(f'Dealer has {player2.hand_total}')
                sleep(.8)
                if player2.hand_total >= 17:
                    break
                if(shoe.check_cut_card()):
                    cut_card = True
                player2.assign_card(shoe.deal())
                
            if player2.status() == 'Bust':
                player2.show_actual_hand()
                print(f"Dealer busts with {player2.hand_total}; You win ${player1.current_wager}!")
                sleep(.8)
                player1.update_bankroll(player1.current_wager)
            elif player2.hand_total > player1.hand_total:
                print(f"The Dealer's {player2.hand_total} beats your {player1.hand_total}; You lose ${player1.current_wager}!")
                sleep(.8)
                player1.update_bankroll(-player1.current_wager)
            elif player2.hand_total < player1.hand_total:
                print(f"Your {player1.hand_total} beats the Dealer's {player2.hand_total}; You win ${player1.current_wager}!")
                sleep(.8)
                player1.update_bankroll(player1.current_wager)
            else:
                print(f"Your {player1.hand_total} is equal to the Dealer's {player2.hand_total}; You Push!")
                sleep(.8)
        else:
            print(f"This hand busted with {player1.hand_total} and you have lost ${player1.current_wager}")
            sleep(.8)
            player1.update_bankroll(-player1.current_wager)
            player2.show_actual_hand()
        player1.change_hands()
        print('\n')
    player1.discard_hand(discard_tray)
    player2.discard_hand(discard_tray)
   

    #Deciding whether or not to continue playing
    if player1.bankroll < table_min:
        print(f"The table minimum is ${table_min} and you don't have enough to place another bet with only ${player1.bankroll} left")
        sleep(.8)
        break
    while True:
        continue_play = input("Would you like to continue playing? (y/n) ").strip().lower()
        if continue_play in {'yes', 'ye', 'y', 'n', 'no', 'nah'}:
            # print(cut_card)
            if cut_card:
                shoe.insert_cards(discard_tray.cards)
                # print(shoe.cards)
                # print(discard_tray.cards)
                shoe.shuffle_shoe()
                sleep(.8)
                cut_card = False
            break
        else:
            print(f'{continue_play} is an invalid response; please try again')
            sleep(.8)
    if continue_play in {'n', 'no', 'nah'}:
        break
print(f'Thank you for playing, {player1.name}! \nYour total winnings are ${player1.winnings} and you leave with ${player1.bankroll}')
sleep(.8)
print('Come back again real soon!')

