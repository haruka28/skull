import random
from player import Player

class Game:
    def __init__(self, num_players):
        self.players = []
        for i in range(num_players):
            self.players.append(Player(i))
        self.cur_player = 0
        self.cur_call = 0
        self.passes = 0
        self.calling = -1
        self.end = False

    def status(self):
        for player in self.players:
            print(player.status())

    def initiate(self):
        # first round, everyone puts down a card
        self.status()
        print("Initiation round")
        for player in self.players:
            player.initiate()
        self.status()

    def curCount(self):
        res = 0
        for player in self.players:
            if (len(player.cards) > 0):
                res += len(player.stash)
        return res

    def proceed(self):
        if self.end: return
        alive = []
        for p in self.players:
            if len(p.cards) > 0:
                alive.append(p.id)
        if len(alive) == 1:
            print("Player {} has won as the only player alive".format(alive[0]))
            self.end = True
            return
        print("Player {}'s turn".format(self.cur_player))
        player = self.players[self.cur_player]
        self.cur_player = (self.cur_player + 1) % len(self.players)
        r = player.play(self)
        if r < 2:
            print("Player {} stashed a card".format(player.id))
        if r == 2:
            print("Player {} passed".format(player.id))
            self.passes += 1
            if self.passes == len(self.players) - 1:
                if self.calling < 0:
                    print("Invalid calling player ID")
                else:
                    self.players[self.calling].challenge(self)
        if r > 2:
            self.cur_call = r - 2
            print("Player {} called {}".format(player.id, self.cur_call))
            self.calling = player.id
            # reset current pass count
            self.passes = 0
        self.status()

    def resetAfterChallenge(self):
        for player in self.players:
            player.reset()
        self.cur_player = self.calling
        self.cur_call = 0
        self.passes = 0
        self.calling = -1

    def start(self):
        self.initiate()
        turn = 1
        while True:
            print("Turn {}".format(turn))
            turn += 1
            self.proceed()
            if self.end: break
            print("")
