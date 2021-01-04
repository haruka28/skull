import random

class Game:
    def __init__(self, players, verbose = True):
        self.players = players
        self.cur_player = 0
        self.cur_call = 0
        self.passed = []
        self.calling = -1
        self.end = False
        self.winner = -1
        self.verbose = verbose

    def status(self):
        for player in self.players:
            self.log(player.status())

    def initiate(self):
        # first round, everyone puts down a card
        self.status()
        self.log("Initiation round")
        for player in self.players:
            player.initiate()
        self.status()

    def getAllStashCount(self):
        res = 0
        for player in self.players:
            if (len(player.cards) > 0):
                res += len(player.stash)
        return res

    def proceed(self):
        if self.winner >= 0: return
        alive = []
        for p in self.players:
            if len(p.cards) > 0:
                alive.append(p.id)
        if len(alive) == 1:
            self.endGame(alive[0], "Player {} has won as the only player alive".format(alive[0]))
            return
        self.log("Player {}'s turn".format(self.cur_player))
        player = self.players[self.cur_player]
        self.cur_player = (self.cur_player + 1) % len(self.players)
        r = player.play(self)
        if r.startswith("s"):
            self.log("Player {} stashed a card".format(player.id))
        if r == "p":
            self.log("Player {} passed".format(player.id))
            if player.id not in self.passed:
                self.passed.append(player.id)
            if len(self.passed) == len(self.players) - 1:
                if self.calling < 0:
                    self.log("Invalid calling player ID")
                else:
                    # challenging player becomes next starting player.
                    # this may be overridden if challenging player is out.
                    self.cur_player = self.calling
                    self.startChallenge()
        if r.startswith("c"):
            self.cur_call = int(r[1:])
            self.log("Player {} called {}".format(player.id, self.cur_call))
            self.calling = player.id
        self.status()

    def startChallenge(self):
        player = self.players[self.calling]
        self.log("Player {} challenging".format(player.id))
        count = 0
        while count < self.cur_call:
            count += 1
            reveal_player = player.reveal(self)
            reveal = self.players[reveal_player].stash.pop()
            if (reveal == 1):
                self.log("Challenging player {} busted by player {}".format(player.id, reveal_player))
                self.cur_player = player.loseChallenge(self, reveal_player)
                self.resetAfterChallenge()
                return
        self.log("Challenging player {} won the challenge".format(player.id))
        player.wins += 1
        if player.wins > 1:
            self.endGame(player.id, "Player {} won the game".format(player.id))
        self.resetAfterChallenge()

    def resetAfterChallenge(self):
        for player in self.players:
            player.reset()
            player.initiate()
        self.cur_call = 0
        self.passed = []
        self.calling = -1

    def getAllPlayersAlive(self):
        res = []
        for player in self.players:
            if len(player.cards) > 0:
                res.append(player.id)
        return res

    def start(self):
        self.initiate()
        turn = 1
        while self.winner == -1:
            self.log("Turn {}".format(turn))
            turn += 1
            self.proceed()
            self.log("")
        return self.winner

    def endGame(self, winner, message):
        self.end = True
        self.winner = winner
        self.log(message)

    def log(self, message):
        if self.verbose:
            print(message)
