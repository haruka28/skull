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

    def status(self):
        if self.wins == 2:
            return "Player {} has won with 2 wins ".format(self.id)
        elif len(self.cards) == 0:
            return "Player {} is out ".format(self.id)
        else:
            return "Player {} has cards {} and stash {} ".format(self.id, self.cards, self.stash)

    # TODO: Move this to move strategy.
    def initiate(self):
        if len(self.cards) > 0:
            self.stashCard(self.cards[random.randint(0, len(self.cards) - 1)])

    def play(self, game):
        if len(self.cards) == 0 or self.id in game.passed:
            # can only pass
            return "p"
        return self.move_strategy(self, game)

    def stashCard(self, card):
        self.stash.append(card)

    def reset(self):
        self.stash = []

    # return next starting player id
    def loseChallenge(self, game, killer):
        del self.cards[random.randint(0, len(self.cards) - 1)]
        # override next starting player
        if len(self.cards) == 0:
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
