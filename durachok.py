import random
import copy

# defines the lowest trump card in a player's hand
def find_lowest_trump(source_list: list, trump_suit: str) -> int:
    minimum_val = None
    for card in source_list:
        if card.suit == trump_suit:
            if minimum_val == None:
                minimum_val = card.value
            elif card.value < minimum_val:
                    minimum_val = card.value
    if minimum_val == None:
        return 0
    else:
        return minimum_val    

# deal cards from the deck          
def deal_card(source_list: list, destination_list: list):
    destination_list.append(source_list.pop())

# finds the index of the lowest value card in a hand
def find_min_card_index(hand_in: list["Card"]) -> int:
    min_card_index = 0
    for card_index in range(len(hand_in)):
        if hand_in[card_index].value < hand_in[min_card_index].value:
            min_card_index = card_index
    return min_card_index

# sorts cards in a hand from lowest to highest value, regardless of suit
# works for any number of cards in a hand list
# !will later add sorting trump cards separately
def get_sorted_hand(players_hand_in: list, trump: "Card") -> list["Card"]:
    players_hand_unsorted = copy.deepcopy(players_hand_in)
    players_hand_sorted = [0]*len(players_hand_unsorted)
    for i in range(len(players_hand_sorted)):
        min_card_index = find_min_card_index(players_hand_unsorted)
        players_hand_sorted[i] = players_hand_unsorted[min_card_index]
        players_hand_unsorted.pop(min_card_index)
    return players_hand_sorted

# shuffles the deck
def shuffle(original_list: list):
    new_list = []
    while len(original_list)>0:
        random_index = random.randint(0, len(original_list)-1)
        new_list.append(original_list[random_index])
        original_list.pop(random_index)
    return new_list

class Player:

    def __init__(self, name: str):
        self.name = name
        self.hand = []

class Card:
    
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def __repr__(self):
        
        visual_value = str(self.value)
        if self.value == 11:
            visual_value = "J"
        if self.value == 12:
            visual_value = "Q"
        if self.value == 13:
            visual_value = "K"
        if self.value == 14:
            visual_value = "A"
        
        visual_suit = self.suit
        if self.suit == "hearts":
            visual_suit = "\033[31m♥"
        if self.suit == "spades":
            visual_suit = "\033[90m♠"
        if self.suit == "diamonds":
            visual_suit = "\033[31m♦"
        if self.suit == "clubs":
            visual_suit = "\033[90m♣"
        return visual_value + visual_suit + "\033[0m"

# initial sequence to:
# - create the deck
# - shuffle the deck
# - define a trump card for the game
# - get players names
# - deal cards and display the hands
# - define who goes first by checking for the lowest trump card
# and redealing the hands if there's no trump card in either hand
def start_game():

    deck = []
    for suit in ["hearts", "diamonds", "spades", "clubs"]:
        for val in range(6,15):
            card = Card(val, suit)
            deck.append(card)

    deck = shuffle(deck)

    trump = deck[0]
    print("The trump card is " + trump.__repr__() + "!")
    print("The trump suit is " + trump.suit + "!\n")

    player_1 = Player(input("Hey Player_1, enter your name!\n").strip())
    player_2 = Player(input("Hey Player_2, now you enter your name!\n").strip())

    while len(player_1.hand) < 6:
        deal_card(deck, player_1.hand)
        deal_card(deck, player_2.hand)
    
    player_1.hand = get_sorted_hand(player_1.hand, trump)
    player_2.hand = get_sorted_hand(player_2.hand, trump)

    print("\n" + player_1.name + ":" + str(player_1.hand))
    print(player_2.name + ":" + str(player_2.hand))

    #a functionality to check for the trump card with the lowest value
    ##display the lowest trumps from each hand
    #if there's no trump card in every hand, re-deal both hands and check again
    #rewrite the who_makes_a_move variable

    p1_lowest_trump_val = find_lowest_trump(player_1.hand, trump.suit)
    p2_lowest_trump_val = find_lowest_trump(player_2.hand, trump.suit)

    if p1_lowest_trump_val == p2_lowest_trump_val:
        print("Oops! Sh*t happens - there are no trump cards! Let's start all over again.")
        start_game()
    elif p1_lowest_trump_val < p2_lowest_trump_val:
        who_moves = player_1
    elif p1_lowest_trump_val > p2_lowest_trump_val:
        who_moves = player_2

    print("\nThe first one to make a move is " + who_moves.name + "!")

    while True: # tut budet is_finished peremennaya, kotoraya buted proveryat, est li karty v rukah oboih igrokov
        print("\n" + who_moves.name + ", it's your turn.")
        print("Here's your hand: " + who_moves.hand)
        print("The trump suit is " + trump.suit) # add background color for trump cards

        break

start_game()

#One turn sequenceh b:

#1.display players hand, trump suit, cards already on the table (in pairs)
#2.decide who makes a move
#   - create a variable: "c"-computer (if human was the last), "h" (if computer was the last)
#   - the variable is only switched if the defence was successful = so there should be a check for that
#3.describe a process of making a move - a separate function
#   function for a human: chooses a card (create a process for that), with a visual
#   function for a computer: chooses the card with the lowest value and not a trump, if possible
#3.1 create a move_list to store all the cards involved in a move
#4.describe a process of defence - a separate function
#5.check if one more move is possible
#6.check if the defence was succressful
#   + rewrite the variable
#   - add all the cards from the move_list to the looser's hand
#7.check how many cards are in each hand and deal the cards until it's at least 6 in each hand
#8. shuffle the cards in both hands