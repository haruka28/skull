import random

class PickStrategy:
    @staticmethod
    def randomize(player, game):
        players_alive = game.getAllPlayersAlive()
        return players_alive[random.randint(0, len(players_alive) - 1)]
