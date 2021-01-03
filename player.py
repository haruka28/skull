import random

class Player:
    def __init__(self, id):
        self.id = id
        self.cards = [0, 0, 0, 1]
        self.stash = []
        self.wins = 0

    def status(self):
        if self.wins == 2:
            return "Player {} has won with 2 wins ".format(self.id)
        elif len(self.cards) == 0:
            return "Player {} is out ".format(self.id)
        else:
            return "Player {} has cards {} and stash {} ".format(self.id, self.cards, self.stash)

    def play(self, can_pass, call_range, can_stash):
        # 2 for pass
        if len(self.cards) == 0:
            # can only pass
            return 2
        moves = []
        if can_pass:
            moves.append(2)
        # call id is actual call + 2, e.g. calling for 1 flower is represented
        # as 3
        moves += call_range
        if can_stash and len(self.cards) > len(self.stash):
            moves += self.cards
            # remove already stashed cards
            for c in self.stash:
                moves.remove(c)
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m < 2:
            self.stash.append(m)
        return m

    def reset(self):
        self.stash = []

    def lose(self):
        del self.cards[random.randint(0, len(self.cards) - 1)]

    def challenge(self, game):
        count = 0
        if len(self.cards) == 0:
            print("Illegal calling player ID")
        print("Player {} challenging".format(self.id))
        # flip own stash
        if 1 in self.stash:
            print("Player {} self-destructed".format(self.id))
        count += len(self.stash)
        if count >= game.cur_call:
            print("Challenging player {} won the challenge with own stash".format(self.id))
        # start challenging the remaining rounds
        for i in range(game.cur_call - len(self.stash)):
            ids = []
            for p in game.players:
                if p.id == self.id:
                    continue
                if len(p.stash) > 0 and len(p.cards) > 0:
                    ids.append(p.id)
            c = ids[random.randint(0, len(ids) - 1)]
            if (game.players[c].stash.pop() == 1):
                print("Challenging player {} busted by player {}".format(self.id, c))
                self.lose()
                break
            else:
                count += 1
        if count == game.cur_call:
            print("Challenging player {} won the challenge".format(self.id))
            self.wins += 1
            if self.wins > 1:
                print ("Player {} won the game".format(self.id))
                game.end  = True
        game.resetAfterChallenge()
