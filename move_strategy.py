import random

class MoveStrategy:
    @staticmethod
    def randomize(player, game):
        if len(player.cards) == 0 or player.id in game.passed:
            # can only pass
            return "p"
        moves = []
        # player can pass as long as there is an active call
        # player can call from cur_call + 1, up to total number of cards
        # player can stash until calling as started
        if game.cur_call > 0:
            moves.append("p")
        if game.cur_call == 0 and len(player.cards) > len(player.stash):
            moves += ["s" + str(x) for x in player.cards]
            # remove already stashed cards
            for c in player.stash:
                moves.remove("s" + str(c))
        call_range = []
        if game.curCount() > game.cur_call:
            call_range = range(game.cur_call + 1, game.curCount() + 1)
        moves += ["c" + str(x) for x in call_range]
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m.startswith("s"):
            player.stashCard(int(m[1:]))
        return m

    @staticmethod
    def noBluff(player, game):
        if len(player.cards) == 0 or player.id in game.passed:
            # can only pass
            return "p"
        moves = []
        # player can pass as long as there is an active call
        # player can call from cur_call + 1, up to total number of cards, as long as they have not already passed this round
        # player can stash until calling as started
        if game.cur_call > 0:
            moves.append("p")
        if game.cur_call == 0 and len(player.cards) > len(player.stash):
            moves += ["s" + str(x) for x in player.cards]
            # remove already stashed cards
            for c in player.stash:
                moves.remove("s" + str(c))
        call_range = []
        if game.curCount() > game.cur_call and not 1 in player.stash:
            call_range = range(game.cur_call + 1, game.curCount() + 1)
        moves += ["c" + str(x) for x in call_range]
        # if player cant stash or pass, then they still need to call.
        if len(moves) == 0:
            moves.append("c" + str(game.cur_call + 1))
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m.startswith("s"):
            player.stashCard(int(m[1:]))
        return m
