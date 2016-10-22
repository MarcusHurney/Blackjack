# Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
show = False
outcome = ""
score = 0
new_game_message = "Click Deal to play a game of Blackjack."
start = False


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:

    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:

    def __init__(self):
        self.hand_cards = []

    def __str__(self):
        ans = ""
        for card in self.hand_cards:
            ans += str(card) + " "
        return "Hand contains: " + ans

    def add_card(self, card):
        self.hand_cards.append(card)

    def get_value(self):
        total = 0

        for card in self.hand_cards:
            total += VALUES[card.get_rank()]

            if card.get_rank() == "A" and (total + 10) <= 21:
                total += 10

        return total


    def draw(self, canvas, pos):
        counter = 1
        for card in self.hand_cards:
            card.draw(canvas, (pos[0]*counter,pos[1]))
            counter += 1.5



# define deck class
class Deck:

    def __init__(self):
        self.deck_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_cards.append(Card(suit, rank))


    def shuffle(self):
        random.shuffle(self.deck_cards)

    def deal_card(self):
        return self.deck_cards.pop()

    def __str__(self):
        ans = ""
        for card in self.deck_cards:
            ans += str(card) + " "
        return "Deck contains: " + ans




#define event handlers for buttons
def deal():

    global outcome, in_play, playing_deck, dealers_hand, players_hand, show, start, score


    playing_deck = Deck()
    dealers_hand = Hand()
    players_hand = Hand()

    playing_deck.shuffle()

    for i in range(2):
        players_hand.add_card(playing_deck.deal_card())
        dealers_hand.add_card(playing_deck.deal_card())


    if in_play == True:
        score -= 1
        in_play = True
    else:
        in_play = True



    show = False
    start = True

    outcome = "A new game has begun. Hit or Stand?"




def hit():

    global score, in_play, outcome, show


    if in_play == True and players_hand.get_value() <= 21:

        players_hand.add_card(playing_deck.deal_card())

        if players_hand.get_value() > 21:
            outcome = "Sorry, the player busted! Dealer wins. Click Deal to play again."
            score -= 1
            show = True
            in_play = False


def stand():

    global in_play, score, outcome, show

    if in_play == True and players_hand.get_value() <= 21:

        while dealers_hand.get_value() <= 17:
            dealers_hand.add_card(playing_deck.deal_card())

        if dealers_hand.get_value() > 21:
                outcome = "Dealer busted! Player wins. Click Deal to play again."
                score += 1
                show = True
                in_play = False



        elif dealers_hand.get_value() == players_hand.get_value():
                outcome = "Tie! But, Dealer wins... Click Deal to play again"
                score -= 1
                show = True
                in_play = False


        elif dealers_hand.get_value() > players_hand.get_value():
                outcome = "Dealer's hand is greater, so dealer wins! Click Deal to play again."
                score -= 1
                show = True
                in_play = False


        elif dealers_hand.get_value() < players_hand.get_value():
                outcome = "Player's hand is greater, so player wins! Click Deal to play again."
                score += 1
                show = True
                in_play = False

def draw(canvas):

    if start == True:
        canvas.draw_text("Score: " + str(score), [275, 500], 20, "black")
        canvas.draw_text("BLACKJACK", [250, 50], 20, "black")
        canvas.draw_text("Player's Hand", [25, 100], 20, "black")
        canvas.draw_text("Dealer's Hand", [25, 250], 20, "black")
        players_hand.draw(canvas, [50, 125])
        dealers_hand.draw(canvas, [50, 275])
        canvas.draw_text(outcome, [25, 450], 20, "black")

        if show == False:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_SIZE, [86, 323], CARD_SIZE)
    else:
        canvas.draw_text(new_game_message, [150, 300], 20, "black")




# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling



frame.start()
