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
    if minimum_val != None:
        return minimum_val
    else:
        return 0 

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


# converts string card into object card
# (returns object card if it is in hand: if it's not there, asks to try again)
# if successful, removes card from hand and appends to the list of field cards
# dumb but works - will later refine it
def fetch_card(card_name: str, hand: list["Card"]) -> "Card":
    
    assert len(card_name) >= 2

    card_value = 0
    card_suit = ""
    
    if len(card_name) == 3:
        card_value = 10
        if card_name[2] == "h":
            card_suit = "hearts"
        elif card_name[2] == "s":
            card_suit = "spades"
        elif card_name[2] == "c":
            card_suit = "clubs"
        elif card_name[2] == "d":
            card_suit = "diamonds"
    
    if len(card_name) == 2:
        if card_name[0] == "J":
            card_value = 11
        elif card_name[0] == "Q":
            card_value = 12
        elif card_name[0] == "K":
            card_value = 13
        elif card_name[0] == "A":
            card_value = 14

        if card_name[1] == "h": #s c d
            card_suit = "hearts"
        elif card_name[1] == "s":
            card_suit = "spades"
        elif card_name[1] == "c":
            card_suit = "clubs"
        elif card_name[1] == "d":
            card_suit = "diamonds"

        if card_name[0] in ["6", "7", "8", "9"]:
            card_value = int(card_name[0])

    for card in hand: # use filter instead later
        if card.value == card_value and card.suit == card_suit:
            return card

    if card_name == "pass":
        return card_name    
    #print("It's either a typo, or there's no such card. Try again!")
    #return None

def print_info(player, trump_card):
    print(f"\n{player.name}, here's your hand: {player.hand}")
    if trump_card.suit == "hearts" or trump_card.suit == "diamonds":
        print(f"The trump suit is \033[37;41m{trump_card.suit}\033[0m.\n")
    elif trump_card.suit == "spades" or trump_card.suit == "clubs":
        print(f"The trump suit is \033[37;100m{trump_card.suit}\033[0m.\n")

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
    
    def __eq__(self, value):
        pass

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
    print(f"The trump card is {trump.__repr__()}!")
    if trump.suit == "hearts" or trump.suit == "diamonds":
        print(f"The trump suit is \033[37;41m{trump.suit}\033[0m.\n")
    elif trump.suit == "spades" or trump.suit == "clubs":
        print(f"The trump suit is \033[37;100m{trump.suit}\033[0m.\n")

    player_1 = Player("God") #(input("Hey Player_1, enter your name!\n").strip())
    player_2 = Player("Devil") #(input("Hey Player_2, now you enter your name!\n").strip())

    while len(player_1.hand) < 6:
        deal_card(deck, player_1.hand)
        deal_card(deck, player_2.hand)
    
    player_1.hand = get_sorted_hand(player_1.hand, trump)
    player_2.hand = get_sorted_hand(player_2.hand, trump)

    print("\n" + player_1.name + ":" + str(player_1.hand))
    print(player_2.name + ":" + str(player_2.hand))

    ##display the lowest trumps from each hand
    #if there's no trump card in every hand, re-deal both hands and check again
    #rewrite the who_makes_a_move variable

    p1_lowest_trump_val = find_lowest_trump(player_1.hand, trump.suit)
    p2_lowest_trump_val = find_lowest_trump(player_2.hand, trump.suit)

    print(f"The lowest trumps are: {player_1.name} - {p1_lowest_trump_val}, {player_2.name} - {p2_lowest_trump_val}.")

    if p1_lowest_trump_val == p2_lowest_trump_val: # both players have zero trumps
        print("Oops! Sh*t happens - there are no trump cards! Let's start all over again.")
        start_game()
    elif p1_lowest_trump_val !=0 and p2_lowest_trump_val !=0: # both players have at least one trump card
        if p1_lowest_trump_val < p2_lowest_trump_val:
            who_moves = player_1
            who_defends = player_2
        elif p1_lowest_trump_val > p2_lowest_trump_val:
            who_moves = player_2
            who_defends = player_1
    elif p1_lowest_trump_val == 0: # p1 has zero trump cards
        who_moves = player_2
        who_defends = player_1
    else: # p2 has zero trump cards
        who_moves = player_1
        who_defends = player_2

    print("\nThe first one to make a move is " + who_moves.name + "!")

    is_game_finished = True

    while is_game_finished == True:

        is_turn_finished = True

        while is_turn_finished == True:
            # when this turn ends, goes back to previous while loop to check if the game has finished
            
            cards_on_the_field = [] #keeps track of all cards currently in play

            # stores cards that are valid for defence
            valid_defence_cards = []

            # stores cards that are valid for attack
            valid_attack_cards = []

            # stores all the cards that have been played - for debugging purpose
            discard_pile = []

            print("\n" + who_moves.name + ", it's your turn to attack.")
            
            # loops through attack-defence sequence until there are valid cards for attack
            while True:
                
                print_info(who_moves, trump)

                if len(cards_on_the_field) > 0 and len(valid_attack_cards) > 0:
                    print(f"These are valid cards for the next attack: {valid_attack_cards}.")
                    input_attack_card = input(f"Pick a card or type PASS to end the attack:")
                
                    if input_attack_card.lower().strip() == "pass":
                        print(f"\n\033[37;42mDefence was successful\033[0m - {who_defends.name}, get ready to attack.")
                        if who_moves == player_1:
                            who_moves = player_2
                            who_defends = player_1
                        else:
                            who_moves = player_1
                            who_defends = player_2
                        discard_pile.append(cards_on_the_field)
                        cards_on_the_field = []
                
                    if len(deck) > 0:
                        while len(who_moves.hand) < 6 and len(deck) > 0:
                            deal_card(deck, who_moves.hand)
                        while len(who_defends.hand) < 6 and len(deck) > 0:
                            deal_card(deck, who_defends.hand)
                    who_moves.hand = get_sorted_hand(who_moves.hand, trump)
                    who_defends.hand = get_sorted_hand(who_defends.hand, trump)
                    
                    cards_on_the_field = []

                else:
                    input_attack_card = input(who_moves.name + ", pick a card to attack:")
                
                if input_attack_card.lower().strip() != "pass":
                    attack_card = fetch_card(input_attack_card, who_moves.hand)

                    if len(valid_attack_cards) > 0 and attack_card in valid_attack_cards:
                        valid_attack_cards.remove(attack_card)
                    if len(valid_attack_cards) > 0 and attack_card not in who_moves.hand:
                        valid_attack_cards.remove(attack_card)

                    print(attack_card)
                    who_moves.hand.remove(attack_card)
                    cards_on_the_field.append(attack_card)

                if if_defence_possible(attack_card, who_defends, trump, valid_defence_cards) == True:

                    print(f"\n{who_defends.name}, defend yourself!")
                    print_info(who_defends, trump)
                    print(f"These cards are valid for defence: {valid_defence_cards}.")

                    input_defend_card = input(f"{who_defends.name}, pick a card for defence - or type PASS to take:")
                    
                    if input_defend_card.lower().strip() == "pass":
                        who_defends.hand = who_defends.hand + cards_on_the_field
                        who_defends.hand = get_sorted_hand(who_defends.hand, trump)
                        # add a check if attacker can put more cards for defender to take
                        print(f"\n{who_defends.name}, you take -\nhere's your hand: {who_defends.hand}")
                        is_turn_finished = False

                    defence_card = fetch_card(input_defend_card, who_defends.hand)
                
                    if defence_card in valid_defence_cards:
                        print(defence_card)
                        who_defends.hand.remove(defence_card)
                        cards_on_the_field.append(defence_card)
                        valid_defence_cards = []
                        
                        for a_card in who_moves.hand:
                            for f_card in cards_on_the_field:
                                if a_card.value == f_card.value and a_card not in cards_on_the_field and a_card not in valid_attack_cards:
                                    valid_attack_cards.append(a_card)
            
                # else:
                #     print(f"{who_defends.name}, it's not a valid choice - try something else.") # what to do with this lol
                #     break

                    if len(valid_attack_cards) == 0:
                        if len(discard_pile) + len(cards_on_the_field) + len(who_defends.hand) < 36:
                            print(f"\n\033[37;42mDefence was successful\033[0m - {who_defends.name}, get ready to attack.")
                            if who_moves == player_1:
                                who_moves = player_2
                                who_defends = player_1
                            else:
                                who_moves = player_1
                                who_defends = player_2
                            discard_pile.append(cards_on_the_field)
                            cards_on_the_field = []
                            # check if there is a possible additional attack
                    
                            # deal the cards if there are any left before quitting this loop
                            if len(deck) > 0:
                                while len(who_moves.hand) < 6 and len(deck) > 0:
                                    deal_card(deck, who_moves.hand)
                                while len(who_defends.hand) < 6 and len(deck) > 0:
                                    deal_card(deck, who_defends.hand)
                            who_moves.hand = get_sorted_hand(who_moves.hand, trump)
                            who_defends.hand = get_sorted_hand(who_defends.hand, trump)
                            
                            cards_on_the_field = []

                else:
                    print(f"\n\033[47;34mDefence is not possible.\033[0m")
                    # add a check if there are attack cards to add when defender takes
                    print(f"{who_defends.name}, you take \u2620.")
                    who_defends.hand = who_defends.hand + cards_on_the_field

                    if len(deck) > 0:
                        while len(who_moves.hand) < 6 and len(deck) > 0:
                            deal_card(deck, who_moves.hand)
                        who_moves.hand = get_sorted_hand(who_moves.hand, trump)
                        who_defends.hand = get_sorted_hand(who_defends.hand, trump)

                    cards_on_the_field = []
                    
                if len(player_1.hand) > 0 and len(player_2.hand) > 0:
                    is_game_finished = True
                elif len(player_1.hand) == 0:
                    print(f"{player_1.name} wins! {player_2.name}, you're a fool.")
                    is_game_finished = False
                    break
                elif len(player_2.hand) == 0:
                    print(f"{player_2.name} wins! {player_1.name}, you're a fool.")
                    is_game_finished = False
                    break
                else:
                    print("It's a tie, wow, how nice and boring. I suggest you try again, guys.")
                    is_game_finished = False
                    break

                is_turn_finished = False

            # TO DO
            # - check for the possible cards for continuing attack, add them to the valid_attack_cards list
            # - deal the cards to those players who have less than 6 cards
            # - check if it's possible to continue with the game (if after attempting to deal the cards both players
            # still have cards on hands)
            # - change who_moves variable depending on the outcome of the clash
            # - if there is at least one player without cards, end the game
            # (create and change bool variable to break the whole game loop)

            # +done FIX THE INITAL CHOICE OF THE FIRST PLAYER TO MOVE!!!

            # break # one clash loop
        
        break # one whole game loop

# checks if there is a possible move for defence (print_info will also go here)
# appends a list of possible defence cards for current move
def if_defence_possible(attack_card, defender, trump, defence_cards_list) -> bool:
    if attack_card.suit != trump.suit:
        for card in defender.hand:
            if card.value > attack_card.value and card.suit == attack_card.suit:
                defence_cards_list.append(card)
            elif card.suit == trump.suit:
                defence_cards_list.append(card)
            
    if attack_card.suit == trump.suit:
        for card in defender.hand:
            if card.suit == trump.suit and card.value > attack_card.value:
                defence_cards_list.append(card)
    
    if len(defence_cards_list) >= 1:
        return True
    else:
        return False

# do I even need this? let's see! lol    
def if_add_attack_possible(player: Player, played_cards: list) -> list:
    pass


if __name__ == "__main__":
    start_game()