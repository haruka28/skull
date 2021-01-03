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

    def initiate(self):
        if len(self.cards) > 0:
            self.stashCard(self.cards[random.randint(0, len(self.cards) - 1)])

    def play(self, game):
        # 2 for pass
        if len(self.cards) == 0:
            # can only pass
            return 2
        moves = []
        # player can pass as long as there is an active call
        # player can call from cur_call + 1, up to total number of cards
        # player can stash until calling as started
        call_range = []
        if game.curCount() > game.cur_call:
            call_range = [game.cur_call + 3, game.curCount() + 2]
        if game.cur_call > 0:
            moves.append(2)
        # call id is actual call + 2, e.g. calling for 1 flower is represented
        # as 3
        moves += call_range
        if game.cur_call == 0 and len(self.cards) > len(self.stash):
            moves += self.cards
            # remove already stashed cards
            for c in self.stash:
                moves.remove(c)
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m < 2:
            self.stashCard(m)
        return m

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
            # TODO: Make this a strategy component.
            if len(self.cards) == 0:
                players_alive = game.getAllPlayersAlive()
                game.cur_player = players_alive[random.randint(0, len(players_alive) - 1)]
            game.resetAfterChallenge()
            return
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
                # if a busted player is out, the killer is the next challenger.
                if len(self.cards) == 0:
                    game.cur_player = c
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
