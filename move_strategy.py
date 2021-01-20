import math
import random

class MoveStrategy:
    @staticmethod
    def randomize(player, game):
        # if no card in stash and self has card, stash a card.
        if len(player.stash) == 0 and len(player.cards) > 0:
            return StashStrategy.defaultStash(player, game)
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
        if game.getAllStashCount() > game.cur_call:
            call_range = range(game.cur_call + 1, game.getAllStashCount() + 1)
        moves += ["c" + str(x) for x in call_range]
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m.startswith("s"):
            player.stashCard(int(m[1:]))
        return m

    @staticmethod
    def noBluffRandomize(player, game):
        # if no card in stash and self has card, stash a card.
        if len(player.stash) == 0 and len(player.cards) > 0:
            return StashStrategy.defaultStash(player, game)
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
        # in this strategy, do not call if there is skull in own stash
        if game.getAllStashCount() > game.cur_call and not 1 in player.stash:
            call_range = range(game.cur_call + 1, game.getAllStashCount() + 1)
        moves += ["c" + str(x) for x in call_range]
        # if player cant stash or pass, then they still need to call.
        if len(moves) == 0:
            moves.append("c" + str(game.cur_call + 1))
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m.startswith("s"):
            player.stashCard(int(m[1:]))
        return m

    @staticmethod
    def safeBluffRandomize(player, game):
        # if no card in stash and self has card, stash a card.
        if len(player.stash) == 0 and len(player.cards) > 0:
            return StashStrategy.defaultStash(player, game)
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
        stash_count = game.getAllStashCount()
        if stash_count > game.cur_call:
            if not 1 in player.stash:
                call_range = range(game.cur_call + 1, stash_count + 1)
            else:
                safe_bluff = math.floor((stash_count - 1) / 5) + 1
                if safe_bluff > game.cur_call:
                    call_range = range(game.cur_call + 1, safe_bluff + 1)
        moves += ["c" + str(x) for x in call_range]
        # if player cant stash or pass, then they still need to call.
        if len(moves) == 0:
            moves.append("c" + str(game.cur_call + 1))
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m.startswith("s"):
            player.stashCard(int(m[1:]))
        return m

    @staticmethod
    def aipincaihuiying(player, game, conservative = False):
        # aipingcaihuiying prefers putting down rose and trusting others
        # if no card in stash and self has card, stash a card.
        if len(player.stash) == 0 and len(player.cards) > 0:
            if 0 in player.cards:
                player.stashCard(0)
                return "s0"
            else:
                player.stashCard(1)
                return "s1"
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
        stash_count = game.getAllStashCount()
        if stash_count > game.cur_call:
            if not 1 in player.stash:
                call_range = range(game.cur_call + 1, stash_count + 1)
            else:
                safe_bluff = math.floor((stash_count - 1) / 5) + 1
                if safe_bluff > game.cur_call:
                    call_range = range(game.cur_call + 1, safe_bluff + 1)
        if not conservative:
            moves += ["c" + str(x) for x in call_range]
        elif len(call_range) > 0:
            moves.append("c" + str(call_range[0]))
        # dont pass if can call
        if len(call_range) > 0 and "p" in moves:
            moves.remove("p")
        # dont stash skull if can stash rose
        if "s0" in moves and "s1" in moves:
            moves.remove("s1")
        # if player cant stash or pass, then they still need to call.
        if len(moves) == 0:
            moves.append("c" + str(game.cur_call + 1))
        # randomize
        m = moves[random.randint(0, len(moves) - 1)]
        if m.startswith("s"):
            player.stashCard(int(m[1:]))
        return m

    @staticmethod
    def passiveSkull(player, game):
        # passive skull strategy just stashes skulls all the time. This will not cause them to win. They are just making others lose xD.
        if game.cur_call == 0:
            if len(player.cards) > len(player.stash):
                if 1 in player.cards and not 1 in player.stash:
                    player.stashCard(1)
                    return "s1"
                else:
                    player.stashCard(0)
                    return "s0"
            else:
                # no cards to play, and calling has not started. player has to call.
                return "c1"
        else:
            # calling has started. just pass.
            return "p"

    @staticmethod
    def passiveSkull50(player, game):
        if player.nonce > 4:
            return MoveStrategy.passiveSkull(player, game)
        else:
            return MoveStrategy.safeBluffRandomize(player, game)

    @staticmethod
    def betterBrute(player, game):
        return MoveStrategy.brute(player, game, conservative = True)

class StashStrategy:
    @staticmethod
    def defaultStash(player, game):
        card = player.cards[random.randint(0, len(player.cards) - 1)]
        player.stashCard(card)
        return "s" + str(card)

