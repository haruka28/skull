from game import Game
from player import Player

RUNS = 10000

if __name__ == "__main__":
    res = [0] * 5
    for i in range(RUNS):
        players = []
        # player 0
        players.append(Player(0))
        # player 1
        players.append(Player(1))
        # player 2
        players.append(Player(2))
        # player 3
        players.append(Player(3))
        # player 4
        players.append(Player(4))
        res[Game(players, False).start()] += 1
    print(res)

