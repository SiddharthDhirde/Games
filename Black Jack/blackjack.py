# Global Variables 
from random import shuffle 
suits = ("Hearts", 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten',
         'Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,
          'Jack':10,'Queen':10,'King':10,'Ace':11}
playing = True

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck:
    def __init__(self):
        # Create a deck of cards by iterating over ranks and suits
        self.deck = [Card(suit, rank) for rank in ranks for suit in suits]     
    def __str__(self): 
        # String representation of the deck
        return "The Deck has:\n" + '\n'.join(str(card) for card in self.deck)     
    def shuffle(self):
        # Shuffle the deck
        shuffle(self.deck)
    def deal(self):
        # Deal a card from the deck
        return self.deck.pop() if self.deck else "No cards left to deal"
    
# Players Hand
class Hand:
    def __init__(self): 
        # Initialize an empty hand
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self,card):
        # Add a card to the hand
        self.cards.append(card)
        self.value += values[card.rank]
        # Track aces
        self.aces += 1 if card.rank == "Ace" else 0
    def adjust_for_ace(self):
        # Adjust the value of aces if necessary
        while self.value>21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    def __init__(self,total=100):
        # Initialize player's chips
        self.total = total
        self.bet = 0
    def win_bet(self):
        # Increase chips if player wins
        self.total += self.bet
    def lose_bet(self):
        # Decrease chips if player loses
        self.total -= self.bet
        
# Function for taking bets
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet?  ")) 
        except ValueError:
            print("Sorry please provide an integer value!")
        else:
            if chips.bet <= 0:
                print("Sorry, your bet must be a positive integer.")
            elif chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

def hit(deck, hand):
    # Deal a card to the hand
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck, hand):    
    global playing  # To control an upcoming while loop
    while True:
        x = input("Hit or Stand? Enter h or s: ")
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("\nPlayer stands, dealer's turn")
            playing = False # Global variable
        else:
            print("Sorry, I did not understand that. Please enter 'h' or 's' only.")
            continue
        break  
        
# Functions to display cards
def show_some(player, dealer):
    print("\nDealer's Hand: ")
    print(" <card hidden>")
    print("", dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

# Functions to handle end of game scenarios
def show_players_value(player, dealer):
    print("Player's hand:", player.value)
    print("Dealer's hand:", dealer.value)

def player_busts(player, dealer, chips):
    print("\n---Player busts!---")
    show_players_value(player, dealer)
    chips.lose_bet()
    
def player_wins(player, dealer, chips):
    print('\n---Player Wins!---')
    show_players_value(player, dealer)
    chips.win_bet()
    
def dealer_busts(player, dealer, chips):
    print('\nPlayer Wins! Dealer busts!')
    show_players_value(player, dealer)
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print('\n---Dealer Wins!---')
    show_players_value(player, dealer)
    chips.lose_bet()
    
def push(player, dealer):
    print("\n---Dealer and Player tie! It's a push.---")
    show_players_value(player, dealer)

# Play Game
while True:
    # Print an Opening Statement
    print("\n----------------------------------------------------------------------------------\n")
    print('Welcome to BlackJack! \n\
          Get as close to 21 as you can without going over!\n\
          Dealer hits until she reaches 17. Aces count as 1 or 11.')
    
    # Create and shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    # Set up the player's chips
    player_chips = Chips()  # Remember, the default value is 100    
    
    # Prompt the player for their bet
    take_bet(player_chips)    
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    # Recall playing variable from our hit_or_stand function
    while playing:  
        # Prompt for player to hit or stand
        hit_or_stand(deck, player_hand)
        # Show cards (but keep one dealer card hidden)      
        show_some(player_hand, dealer_hand)
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
        
    # If player hasn't busted, play dealer's hand until dealer reaches 17 
    if player_hand.value <= 21:
        while dealer_hand.value < 17: 
            hit(deck, dealer_hand)
        # Show all cards
        show_all(player_hand, dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
            
    # Inform player of their total chips
    print("\nPlayer's winnings stand at", player_chips.total)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("\nThank you for playing!")
        break
    