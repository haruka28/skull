import random
from game import Game
from player import Player
from move_strategy import MoveStrategy
from pick_strategy import PickStrategy
from reveal_strategy import RevealStrategy
from discard_strategy import DiscardStrategy

RUNS = 10000

if __name__ == "__main__":
    res = [0] * 5
    for i in range(RUNS):
        players = []
        # control
        players.append(Player(0, move_strategy=MoveStrategy.passiveSkull))
        for i in range(1, 4):
            players.append(Player(i, move_strategy=MoveStrategy.safeBluffRandomize))
        # experiment
        players.append(Player(4, move_strategy = MoveStrategy.aipincaihuiying))
        starting = random.randint(0, 4)
        res[Game(players, RUNS <= 10, starting).start()] += 1
    print(res)
