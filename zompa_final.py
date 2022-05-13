import random

class Card():
    card_to_name = {1:"A", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7",
                    8:"8", 9:"9", 10:"10", 11:"J", 12:"Q", 13:"K"}

    def __init__(self, value, suit):
        self.name = self.card_to_name[value]
        self.suit = suit
        self.title = "%s%s" % (self.name, self.suit)
        self.value = value

    def isBelow(self, card):
        return self.value == (card.value - 1)

    def isOppositeSuit(self, card):
        if self.suit == "♣" or self.suit == "♠":
            return card.suit == "♥" or card.suit == "♦"
        else:
            return card.suit == "♠" or card.suit == "♣"

    def canAttach(self, card):
        if card.isBelow(self) and card.isOppositeSuit(self):
            return True
        else:
            return False

    def __str__(self):
        return self.title

class Deck():
    unshuffled_deck = [Card(card, suit) for card in range(1, 14) for suit in ["♣", "♦", "♥", "♠"]]

    def __init__(self, num_decks=1):
        self.deck = self.unshuffled_deck * num_decks
        random.shuffle(self.deck)

    def flip_card(self):
        return self.deck.pop()

    def deal_cards(self, num_cards):
        return [self.deck.pop() for x in range(0, num_cards)]

    def __str__(self):
        return str(self.deck)

class Tableau():
    def __init__(self, card_list):
        self.unflipped = {x: card_list[x] for x in range(7)}
        self.flipped = {x: [self.unflipped[x].pop()] for x in range(7)}

    def flip_card(self, col):
        if len(self.unflipped[col]) > 0:
            self.flipped[col].append(self.unflipped[col].pop())

    def pile_length(self):
        return max([len(self.flipped[x]) + len(self.unflipped[x]) for x in range(7)])

    def addCards(self, cards, column):
        column_cards = self.flipped[column]
        if len(column_cards) == 0 and cards[0].value == 13:
            column_cards.extend(cards)
            return True
        elif len(column_cards) > 0 and column_cards[-1].canAttach(cards[0]):
            column_cards.extend(cards)
            return True
        else:
            return False

    def tableau_to_tableau(self, c1, c2):
        c1_cards = self.flipped[c1]

        for index in range(len(c1_cards)):
            if self.addCards(c1_cards[index:], c2):
                self.flipped[c1] = c1_cards[0:index]
                if index == 0:
                    self.flip_card(c1)
                return True
        return False

    def tableau_to_foundation(self, foundation, column):
        column_cards = self.flipped[column]
        if len(column_cards) == 0:
            return False

        if foundation.addCard(column_cards[-1]):
            column_cards.pop()
            if len(column_cards) == 0:
                self.flip_card(column)
            return True
        else:
            return False

    def waste_to_tableau(self, waste_pile, column):
        card = waste_pile.waste[-1]
        if self.addCards([card], column):
            waste_pile.pop_waste_card()
            return True
        else:
            return False

class DrawWaste():
    def __init__(self, cards):
        self.deck = cards
        self.waste = []

    def draw_to_waste(self):

        if len(self.deck) + len(self.waste) == 0:
            print("No more cards to draw from")
            return False

        if len(self.deck) == 0:
            self.waste.reverse()
            self.deck = self.waste.copy()
            self.waste.clear()

        self.waste.append(self.deck.pop())
        return True

    def pop_waste_card(self):
        if len(self.waste) > 0:
            return self.waste.pop()

    def getWaste(self):
        if len(self.waste) > 0:
            return self.waste[-1]
        else:
            return "Empty"

    def getDrawPile(self):
        if len(self.deck) > 0:
            return str(len(self.deck)) + " cards"
        else:
            return "Empty"

class Foundations():
    def __init__(self):
        self.foundation_stacks = {"♣":[], "♥":[], "♠":[], "♦":[]}

    def addCard(self, card):
        stack = self.foundation_stacks[card.suit]
        try:
            if (len(stack) == 0 and card.value == 1) or stack[-1].isBelow(card):
                stack.append(card)
                return True
            else:
                return False
        except:
            return False

    def getTopCard(self, suit):
        stack = self.foundation_stacks[suit]
        if len(stack) == 0:
            return suit[0].upper()
        else:
            return self.foundation_stacks[suit][-1]

    def isWon(self):
        for suit, stack in self.foundation_stacks.items():
            if len(stack) == 0:
                return False
            card = stack[-1]
            if card.value != 13:
                return False
        return True

def printValidCommands():
    print("d: draw card")
    print("wf: move from waste to foundation")
    print("wt #t: move from waste to tableau")
    print("tf #t: move from tableau to foundation")
    print("tt #t #t: move from tableau to tableau")
    print("cmd: valid commands")
    print("quit: ends game")

def printGame(tableau, foundation, stock_waste):
    print("\n")
    print(f'\nDraw Pile: {stock_waste.getDrawPile()}\nWaste Pile:  {stock_waste.getWaste()}')
    print("{}\t{}\t{}\t{}".format(foundation.getTopCard("♣"), foundation.getTopCard("♥"), foundation.getTopCard("♠"), foundation.getTopCard("♦")))
    print("\n\n\t1\t2\t3\t4\t5\t6\t7\n")
    for x in range(tableau.pile_length()):
        print_str = ""
        for col in range(7):
            hidden_cards = tableau.unflipped[col]
            shown_cards = tableau.flipped[col]
            if len(hidden_cards) > x:
                print_str += "\t-"
            elif len(shown_cards) + len(hidden_cards) > x:
                print_str += "\t" + str(shown_cards[x-len(hidden_cards)])
            else:
                print_str += "\t"
        print(print_str)
    print("\n")

if __name__ == "__main__":
    d = Deck()
    t = Tableau([d.deal_cards(x) for x in range(1,8)])
    f = Foundations()
    sw = DrawWaste(d.deal_cards(24))

    print("\n")
    printValidCommands()
    printGame(t, f, sw)

    while not f.isWon():
        command = input("Enter command: ")
        command = command.lower().replace(" ", "")
        if command == "h":
            printValidCommands()
        elif command == "quit":
            print("Ended game")
            break
        elif command == "d":
            if sw.draw_to_waste():
                printGame(t, f, sw)
        elif command == "wf":
            try:
                if f.addCard(sw.getWaste()):
                    sw.pop_waste_card()
                    printGame(t, f, sw)
                else:
                    print("Invalid move")
            except:
                print("Invalid move")
        elif "wt" in command and len(command) == 3:
            try:
                col = int(command[-1]) - 1
                if t.waste_to_tableau(sw, col):
                    printGame(t, f, sw)
                else:
                    print("Invalid move")
            except:
                print("Invalid move")
        elif "tf" in command and len(command) == 3:
            try:
                col = int(command[-1]) - 1
                if t.tableau_to_foundation(f, col):
                    printGame(t, f, sw)
                else:
                    print("Invalid move")
            except:
                print("Invalid move")
        elif "tt" in command and len(command) == 4:
            try:
                c1, c2 = int(command[-2]) - 1, int(command[-1]) - 1
                if t.tableau_to_tableau(c1, c2):
                    printGame(t, f, sw)
                else:
                    print("Invalid move")
            except:
                print("Invalid move")
        else:
            print("Invalid command")

    if f.isWon():
        print("Game won")