from enum import Enum
import random
from move_strategy import MoveStrategy
from reveal_strategy import RevealStrategy
from pick_strategy import PickStrategy
from discard_strategy import DiscardStrategy

# A strategy composes of N components:
#   - How to make a move (pass, stash, call)
#   - How to reveal during a challenge
#   - How to pick the next player
#   - How to discard one's own card (currently not implemented)

class Player:
    def __init__(self, id,
            move_strategy = MoveStrategy.randomize,
            reveal_strategy = RevealStrategy.randomize,
            pick_strategy = PickStrategy.randomize,
            discard_strategy = DiscardStrategy.randomize):
        self.id = id
        self.cards = [0, 0, 0, 1]
        self.stash = []
        self.wins = 0
        self.move_strategy = move_strategy
        self.reveal_strategy = reveal_strategy
        self.pick_strategy = pick_strategy
        self.discard_strategy = discard_strategy
        # resets per challenge
        self.nonce = random.randint(0, 9)

    def status(self):
        if self.wins == 2:
            return "Player {} has won with 2 wins ".format(self.id)
        elif len(self.cards) == 0:
            return "Player {} is out ".format(self.id)
        else:
            return "Player {} has cards {} and stash {} ".format(self.id, self.cards, self.stash)

    def play(self, game):
        if self.isOut() or self.id in game.passed:
            # can only pass
            return "p"
        return self.move_strategy(self, game)

    def isOut(self):
        return len(self.cards) == 0

    def shouldInitiate(self):
        # if no card is in stash and has card in hand, stash a card to initiate this round.
        return len(self.stash) == 0 and len(self.cards) > 0

    def getHand(self):
        # get all cards in hand. That is, not in stash.
        res = self.cards.copy()
        for i in self.stash:
            res.remove(i)
        return res

    def stashCard(self, card):
        self.stash.append(card)

    def reset(self):
        self.stash = []
        self.nonce = random.randint(0, 9)

    # return next starting player id
    def loseChallenge(self, game, killer):
        del self.cards[random.randint(0, len(self.cards) - 1)]
        # override next starting player
        if self.isOut():
            if killer == self.id:
                # if a self busted player is out, they pick the next challenger.
                return self.pick_strategy(self, game)
            else:
                # if a busted player is out, the killer is the next challenger.
                return killer
        return self.id

    # return player id to reveal
    def reveal(self, game):
        # needs to flip own stash first
        if len(self.stash) > 0:
            return self.id
        else:
            return self.reveal_strategy(self, game)
