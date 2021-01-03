from game import Game

if __name__ == "__main__":
    game = Game(5)
    game.round0()
    for i in range(100):
        print("Turn " + str(i))
        game.play()
