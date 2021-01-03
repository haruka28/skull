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
        return self.move_strategy(self, game)

    def stashCard(self, card):
        self.stash.append(card)

    def reset(self):
        self.stash = []

    def lose(self):
        del self.cards[random.randint(0, len(self.cards) - 1)]

    def challenge(self, game):
        # challenger becomes next player
        game.cur_player = self.id
        count = 0
        if len(self.cards) == 0:
            print("Illegal calling player ID")
        print("Player {} challenging".format(self.id))
        # flip own stash
        if 1 in self.stash:
            print("Player {} self-destructed".format(self.id))
            self.lose()
            # if a self busted player is out, they pick the next challenger.
            if len(self.cards) == 0:
                self.pick_strategy(self, game)
            game.resetAfterChallenge()
            return
        count += len(self.stash)
        if count >= game.cur_call:
            print("Challenging player {} won the challenge with own stash".format(self.id))
        # start challenging the remaining rounds
        for i in range(game.cur_call - len(self.stash)):
            reveal_player = self.reveal_strategy(self, game)
            reveal = game.players[reveal_player].stash.pop()
            if (reveal == 1):
                print("Challenging player {} busted by player {}".format(self.id, reveal_player))
                self.lose()
                # if a busted player is out, the killer is the next challenger.
                if len(self.cards) == 0:
                    game.cur_player = reveal_player
                game.resetAfterChallenge()
                return
            else:
                count += 1
        if count != game.cur_call:
            print("Error?")
        print("Challenging player {} won the challenge".format(self.id))
        self.wins += 1
        if self.wins > 1:
            print ("Player {} won the game".format(self.id))
            game.end = True
        game.resetAfterChallenge()
