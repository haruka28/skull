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

    def round0(self):
        # first round, everyone puts down a card
        game.status()
        print("Initiation round")
        for player in self.players:
            player.play(False, [], True)
        game.status()

    def curCount(self):
        res = 0
        for player in self.players:
            if (len(player.cards) > 0):
                res += len(player.stash)
        return res

    def play(self):
        if self.end:
            return
        alive = []
        for p in self.players:
            if len(p.cards) > 0:
                alive.append(p.id)
        if len(alive) == 1:
            print("Player " + str(alive[0]) +
                    " has won as the only player alive")
            self.end = True
            return
        print("Player " + str(self.cur_player) + "'s turn")
        player = self.players[self.cur_player]
        self.cur_player += 1
        if self.cur_player > len(self.players) - 1:
            self.cur_player = self.cur_player - len(self.players)
        # player can pass as long as there is an active call
        # player can call from cur_call + 1, up to total number of cards
        # player can stash until calling as started
        call_range = []
        if self.curCount() > self.cur_call:
            call_range = [self.cur_call + 3, self.curCount() + 2]
        r = player.play(self.cur_call > 0, call_range, self.cur_call == 0)
        if r < 2:
            print("Player " + str(player.id) + " stashed a card")
        if r == 2:
            print("Player " + str(player.id) + " passed")
            self.passes += 1
            if self.passes == len(self.players) - 1:
                self.challenge()
        if r > 2:
            self.cur_call = r - 2
            print("Player " + str(player.id) + " called " + str(self.cur_call))
            self.calling = player.id
            # reset current pass count
            self.passes = 0
        game.status()

    def challenge(self):
        count = 0
        if self.calling < 0 or self.calling > len(self.players) - 1 or \
                len(self.players[self.calling].cards) == 0:
            print("Illegal calling player ID")
        player = self.players[self.calling]
        print("Player " + str(self.calling) + " challenging")
        print("Player " + str(player.id) + " challenging")
        # current calling player challenges
        # flip own stash
        if 1 in player.stash:
            print("Player " + str(self.calling) + " self-destructed")
        count += len(player.stash)
        # start challenging the remaining rounds
        for i in range(self.cur_call - len(player.stash)):
            ids = []
            for p in self.players:
                if p.id == self.calling:
                    continue
                if len(p.stash) > 0 and len(p.cards) > 0:
                    ids.append(p.id)
            c = ids[random.randint(0, len(ids) - 1)]
            if (self.players[c].stash.pop() == 1):
                print("Challenging player " + str(self.calling) + \
                        " busted by player " + str(c))
                print("Challenging player " + str(player.id) + \
                        " busted by player " + str(c))
                player.lose()
                break
            else:
                count += 1
        if count == self.cur_call:
            print("Challenging player " + str(self.calling) + \
                    " won the challenge")
            player.wins += 1
            if player.wins > 1:
                print ("Player " + str(self.calling) + " won the game")
                self.end  = True
        for player in self.players:
            player.reset()
        self.cur_player = self.calling
        self.cur_call = 0
        self.passes = 0
        self.calling = -1
