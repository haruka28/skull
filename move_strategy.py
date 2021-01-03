import random

class MoveStrategy:
    @staticmethod
    def randomize(player, game):
        # 2 for pass
        if len(player.cards) == 0:
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
        if game.cur_call == 0 and len(player.cards) > len(player.stash):
            moves += player.cards
            # remove already stashed cards
            for c in player.stash:
                moves.remove(c)
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m < 2:
            player.stashCard(m)
        return m

