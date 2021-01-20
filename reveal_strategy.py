import random

class RevealStrategy:
    @staticmethod
    def randomize(player, game):
        ids = []
        for p in game.players:
            if p.id == player.id:
                continue
            if len(p.stash) > 0 and not p.isOut():
                ids.append(p.id)
        c = ids[random.randint(0, len(ids) - 1)]
        return c
