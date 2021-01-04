from game import Game
from player import Player

NUM_PLAYERS = 5

if __name__ == "__main__":
    players = []
    for i in range(NUM_PLAYERS):
        players.append(Player(i))
    game = Game(players)
    game.start()

