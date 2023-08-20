# !/usr/bin/env python3
# 
# still want to code: a class just for the Basic Strategy chart
#

from random import shuffle, randint
from datetime import timedelta, date
from time import sleep

#An individual playing card
class Card():

    #All of the potential point values a card can hold in BJ
    POINT_VALUES = {

        'Ace' : 11, #An ace can either count as a 1 or an 11, for now we are handling this in another method "hand_total"
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

    SUITS = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

    def __init__(self, value, suit):
        self.value = value
        self.points = self.POINT_VALUES[value]
        self.suit = suit
    
    def __repr__(self):
        return f'{self.value} of {self.suit}'
    
# A special card of no value, usually just a solid color fill, 
# that when it comes out of the shoe signals to the dealer to shuffle once that round of play has ended

class Cut_Card(Card):

    def __init__(self):
        self.value = 0
        self.points = 0
        self.suit = None
        self.color = 'Yellow'
    
    def __repr__(self):
        return f'A {self.color} card with {self.value} value and {self.suit} suit; signals to the dealer to shuffle once the current round of play has ended'

class Deck():

    def __init__(self):
        self.cards = []
        self.generate_deck()
        self.shuffle_deck()

    def generate_deck(self):
        for value in Card.POINT_VALUES:
            for suit in Card.SUITS:
                self.cards.append(Card(value,suit))
    
    def shuffle_deck(self):
        order = [i for i in range(52)]
        shuffle(order)
        cards_to_shuffle = [(order[i],self.cards[i]) for i in range(52)]
        cards_to_shuffle.sort()
        self.cards = [cards_to_shuffle[i][1] for i in range(52)]

# A class that will contain multiple decks of cards, don't ask me why they call it a shoe lol


class Shoe():

    shuffle_card = Cut_Card()

    def __init__(self,size):
        self.size = size
        self.num_cards = size*52
        self.cards = []
        self.generate_shoe()
        self.shuffle_shoe()

    def generate_shoe(self):
        for i in range(self.size):
            for card in Deck().cards:
                self.cards.append(card)

    def shuffle_shoe(self):
        print('Shuffling cards...')
        sleep(1)
        order = [i for i in range(self.num_cards)]
        shuffle(order)
        cards_to_shuffle = [(order[i],self.cards[i]) for i in range(self.num_cards)]
        cards_to_shuffle.sort()
        self.cards = [cards_to_shuffle[i][1] for i in range(self.num_cards)]
        self.cards.insert(randint(25,51),self.shuffle_card)
        # self.cards.append(self.shuffle_card)
    
    def deal(self):
        return self.cards.pop(-1)
    
    def check_cut_card(self):
        if self.cards[-1] == self.shuffle_card:
            print('The cut card has come out; this is the last round of play before the shuffle')
            self.cards.pop(-1)
            return True
        
    def insert_cards(self, cards):
        while cards:
            shoe.cards.append(cards.pop())
        
class DiscardTray():

    def __init__(self):
        self.name = 'discard_tray'
        self.cards = []

    def insert_card(self, discarded_card):
            self.cards.append(discarded_card)
    
    def empty_tray(self, shoe):
        for discarded_card in self.cards:
            shoe.cards.append(discarded_card)
    
    def __repr__(self):
        return f'{self.cards}'

class Player():

    def __init__(self, name):
        self.name = name
        self.bankroll = 0
        self.winnings = 0
        self.hands = [[],[],[],[]]
        self.current_hand = self.hands[0]
        self.hand_total = 0
        self.hand_totals = [0,0,0,0]
        self.wagers = [0,0,0,0]
        self.current_wager = self.wagers[0]

    def assign_card(self, card):
        self.current_hand.append(card)
        self.total_of_cards()
    
    def show_hand(self):
        print(f"Your current hand: {self.current_hand}")
        if self.current_hand == Cut_Card():
            print("The cut card has come out; this is the last round before the shuffle")
            return self.current_hand.pop(-1)

    def assign_bankroll(self,bankroll):
        if bankroll > 0:
            self.bankroll = bankroll
        else:
            print("You cannot have a bankroll less than $1")

    def update_bankroll(self, change):
        self.bankroll += change
        self.winnings += change

    def initial_wager(self, table_min, table_limit):
        while True:
            try:
                bet = float(input(f'How much would you like to bet? You currently have ${self.bankroll} $'))
                if bet < table_min:
                    print(f'You cannot place a bet less than the table minimum of ${table_min}')
                elif bet > table_limit:
                    print(f'You cannot bet more than the table limit of ${table_limit}')
                elif bet > player1.bankroll:
                    print(f'You cannot exceed your bankroll: you have ${player1.bankroll}; you tried to place a bet of ${bet}')
                else:
                    print(f'A bet of ${bet} has been placed; good luck to you')
                    return bet
            except:
                print('You did not input a valid wager; please try again')

    def increase_hand_wager(self, wager):
        index = self.wagers.index(self.current_wager)
        self.wagers[index] += wager
        self.current_wager = self.wagers[index]

    def hand_split(self, current_hand, wager):
        if len(current_hand) > 2:
            print('You can not split a hand larger than 2 cards')
            return 0
        elif [] not in self.hands:
            print('You have already split to the maximum of 4 hands')
            return 0
        elif current_hand[0].points != current_hand[1].points:
            print(f'You can not split {current_hand[0].value}, {current_hand[1].value}')
            return 0
        index = self.hands.index(current_hand)
        for i in range(index,len(self.hands)-1):
            if self.hands[i+1] == []:
                self.hands[i+1].append(self.hands[index].pop(-1))
                print(f'You put up the additional {wager} for the split')
                self.wagers[i+1] += wager
                break
        self.show_of_hands()
        return wager

    def show_of_hands(self):
        print(f'Your hands are: {self.hands}')
                
    def discard_hand(self, discard_tray):
        for hand in self.hands:
            while hand:
                discard_tray.insert_card(hand.pop())
        self.wagers = [0,0,0,0]
        self.current_wager = self.wagers[0]
    
    def total_of_cards(self):

        sum = 0
        card_values = [card.value for card in self.current_hand]
        for card in self.current_hand:
            sum += card.points
        if sum > 21 and 'Ace' in card_values:
            ace_count =  card_values.count('Ace')
            while sum > 21 and ace_count > 0:
                sum -= 10
                ace_count -=1
        # print(sum)
        self.hand_total = sum

    def status(self):

        if self.hand_total > 21:
            return 'Bust'
        else:
            return 'Good'
    
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
    def __init__(self):
        super().__init__('Dealer')
    
    def show_hand(self):
        if len(self.current_hand) == 1:
            print(f"Dealer's Hand: ['hidden']")
        elif len(self.current_hand) == 2:
            print(f"Dealer's Hand: ['hidden', {self.current_hand[1]}]")
        else:
            print(f"Dealer's Hand: {self.current_hand}")
    
    def show_actual_hand(self):
        print(f"Dealer's Hand: {self.current_hand}")

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
    cut_card = False
    if(shoe.check_cut_card()):
        cut_card = True
    player1.assign_card(shoe.deal())
    player1.show_hand()
    sleep(1)
    if(shoe.check_cut_card()):
        cut_card = True
    player2.assign_card(shoe.deal())
    player2.show_hand()
    sleep(1)
    if(shoe.check_cut_card()):
        cut_card = True
    player1.assign_card(shoe.deal())
    player1.show_hand()
    sleep(1)
    if(shoe.check_cut_card()):
        cut_card = True
    player2.assign_card(shoe.deal())
    player2.show_hand()
    sleep(1)
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
sleep(1)
print(f'Nice to meet you, {name}')
sleep(1)
table_min = 5
table_limit = 1000
print(f'The table minimum is ${table_min} and the table limit is ${table_limit}')
sleep(1)
while True:
    try:
        bankroll = int(input("How much money did you bring with you to play today? $"))
        if bankroll >= table_min:
            player1.assign_bankroll(bankroll)
            break
        else: 
            print(f'Please input least the table min of ${table_min} for your money')
            sleep(1)
    except:
        print('Please input a valid integer for your money')
        sleep(1)
sleep(1)
print(f'Awesome; cashing in ${bankroll}')
player2 = Dealer()    
deck_count = 0
while True:
    try:
        deck_count = int(input("How many decks do you want to play with today? You can choose an integer between 1 and 8: "))
        if player1.bankroll >= 1:
            break
    except:
        print('Please input a valid integer for the number of decks you want to play with')
        sleep(1)   
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
    sleep(1)
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
                        sleep(1)
                if even_money in {'n', 'no', 'nah'}:
                    if dealer_blackjack:
                        player2.show_actual_hand()
                        print("Dealer has Blackjack: you push")
                        break
                    else:
                        wager *=1.5
                        print(f'BLACKJACK!  You win ${wager}')
                        player1.update_bankroll(wager)
                        player2.show_actual_hand()
                        break
                else:
                    print(f'Taking even money: you win ${wager}')
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
                        sleep(1)
                if insurance in {'n', 'no', 'nah'} or player1.bankroll - wager*1.5 < 0:
                    if player1.bankroll - wager*1.5 < 0:
                        print("You don't have enough money for the insurance bet")
                    if dealer_blackjack:
                        player2.show_actual_hand()
                        print(f"Dealer has Blackjack: you lose ${wager}")
                        player1.update_bankroll(-wager)
                        break
                    else:
                        print("Nobody's home")
                        
                else:
                    print(f"You put up ${wager/2} for insurance")
                    if dealer_blackjack:
                        player2.show_actual_hand()
                        print(f"Dealer has Blackjack; nice call")
                        break
                    else:
                        print(f"Nobody's home: you lose your insurance bet of ${wager/2}")
                        player1.update_bankroll(-wager/2)
                        

            #Handling Dealer Blackjack with 10 showing instead of ace:
            elif dealer_blackjack:
                if blackjack:
                    player2.show_actual_hand()
                    print("Dealer has Blackjack: you push")
                    break
                else:
                    player2.show_actual_hand()
                    print(f"Dealer has Blackjack: you lose ${wager}")
                    player1.update_bankroll(-wager)
                    break
            elif not dealer_blackjack and player2.current_hand[1].points == 10:
                print("Nobody's Home")
            initial_deal_1 = False
    
        if hand == []:
            continue
        elif len(hand) == 1:
            if(shoe.check_cut_card()):
                cut_card = True
            player1.assign_card(shoe.deal())
            # player1.assign_card(Card('Ace','Clubs'))
        player1.show_hand()
        player2.show_hand()
        while player1.status() != 'Bust':
            if len(hand) == 1:
                if(shoe.check_cut_card()):
                    cut_card = True
                player1.assign_card(shoe.deal())
                # player1.assign_card(Card('Ace','Clubs'))
                player1.show_hand()
            choice = input(f'What would you like to do? Your hand total is {player1.hand_total}\n Hit, Stand, Surrender, Split or Double Down ').lower().strip()

            if choice == 'hit':
                if(shoe.check_cut_card()):
                    cut_card = True
                player1.assign_card(shoe.deal())
            elif choice == 'stand':
                print(f'{player1.name} stands with {player1.hand_total}')
                break
            elif choice == 'surrender':
                if len(player1.current_hand) == 2 and initial_deal_2:
                    wager /= 2
                    print(f"You have chosen to surrender; here is ${wager} back")
                    player1.update_bankroll(-wager)
                    surrender = True
                    initial_deal_2 = False
                    player2.show_actual_hand()
                    break
                else:
                    print('You cannot surrender after you have played on your initial two cards')
            elif choice == 'split':
                if total_wagered + wager > player1.bankroll:
                    print(f"You don't have the additional ${wager} in your bankroll to split; you currently have ${player1.bankroll - total_wagered} left")
                else:
                    # player1.hand_split(player1.current_hand, wager)
                    total_wagered += player1.hand_split(player1.current_hand, wager)
            elif choice == 'double down': #This needs to be fixed for the case where the bankroll is less than the wager
                if len(player1.current_hand) == 2 :
                    try: 
                        doubling_for = float(input(f"How much would you like to double down for? You can double down between $1 and ${wager}: $"))
                        if total_wagered + doubling_for > player1.bankroll:
                            print(f"You don't have the additional ${doubling_for} in your bankroll to double down; you currently have ${player1.bankroll - total_wagered} left")
                        elif doubling_for < wager and doubling_for >= 1:
                            print(f"Doubling for less with ${doubling_for}")
                            if(shoe.check_cut_card()):
                                cut_card = True
                            player1.assign_card(shoe.deal())
                            player1.increase_hand_wager(doubling_for)
                            total_wagered += doubling_for
                            break
                        elif doubling_for == wager:
                            print(f'Doubling down: you put up ${wager} for the Double Down')
                            if(shoe.check_cut_card()):
                                cut_card = True
                            player1.assign_card(shoe.deal())
                            player1.increase_hand_wager(wager)
                            total_wagered += wager
                            break
                        else:
                            print(f'${doubling_for} is not a valid amount to Double Down')
                    except:
                        print(f'{doubling_for} is not a valid input; you can double down between $1 and ${wager}')
                else:
                    print('You have more than 2 cards in your hand; you cannot Double Down')
            else:
                print(f'{choice} is not a valid selection, please try again')
            initial_deal = False
            sleep(1)
            player1.show_hand()
            sleep(1)
            player2.show_hand()
            sleep(1)
        player1.change_hands()
        player1.show_of_hands()

    #After player play decision matrix
    player1.current_wager = player1.wagers[0]
    player1.current_hand = player1.hands[0]
    if not blackjack and not dealer_blackjack and not surrender:
        print(f'Play will now go to the dealer')
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
                sleep(1)
                print(f'Dealer has {player2.hand_total}')
                if player2.hand_total >= 17:
                    break
                if(shoe.check_cut_card()):
                    cut_card = True
                player2.assign_card(shoe.deal())
                sleep(1)
                
            if player2.status() == 'Bust':
                player2.show_actual_hand()
                print(f"Dealer busts with {player2.hand_total}; You win ${player1.current_wager}!")
                player1.update_bankroll(player1.current_wager)
            elif player2.hand_total > player1.hand_total:
                print(f"The Dealer's {player2.hand_total} beats your {player1.hand_total}; You lose ${player1.current_wager}!")
                player1.update_bankroll(-player1.current_wager)
            elif player2.hand_total < player1.hand_total:
                print(f"Your {player1.hand_total} beats the Dealer's {player2.hand_total}; You win ${player1.current_wager}!")
                player1.update_bankroll(player1.current_wager)
            else:
                print(f"Your {player1.hand_total} is equal to the Dealer's {player2.hand_total}; You Push!")
        else:
            print(f"This hand busted with {player1.hand_total} and you have lost ${player1.current_wager}")
            player1.update_bankroll(-player1.current_wager)
        player1.change_hands()
        print('\n')
        sleep(1)
    player1.discard_hand(discard_tray)
    player2.discard_hand(discard_tray)
    sleep(1)

    #Deciding whether or not to continue playing
    if player1.bankroll < table_min:
        print(f"The table minimum is ${table_min} and you don't have enough to place another bet with only ${player1.bankroll} left")
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
                sleep(1)
                cut_card = False
            break
        else:
            print(f'{continue_play} is an invalid response; please try again')
            sleep(1)
    if continue_play in {'n', 'no', 'nah'}:
        break
print(f'Thank you for playing, {player1.name}! \nYour total winnings are ${player1.winnings} and you leave with ${player1.bankroll}')
print('Come back again real soon!')

