class Character:
    canSeeMinions = False
    visableToMerlin = False
    visableToPercival = False
    canAssassinate = False
    help_text = "To be implemented"

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__

    def alignment(self):
        return "good" if self.good else "evil"

    def explain_role(self, players):
        if type(self) == Oberon or type(self) == LoyalServantOfArthur:
            return

        print("For {} eyes only:".format(self))
        for player in players:
            if not self.good and not player.card.good and type(player.card) != Oberon:
                print(" - {} appears to be Evil".format(player.name))
            elif type(self) == Merlin and player.card.visableToMerlin:
                print(" - {} appears to be Evil".format(player.name))
            elif type(self) == Percival and player.card.visableToPercival:
                print(" - {} appears to be Merlin".format(player.name))


class LoyalServantOfArthur(Character):
    good = True
    help_text = "Loyal servant of Arthur (good)."

class MinionOfMordred(Character):
    good = False
    canSeeMinions = True
    visableToMerlin = True
    help_text = "Minion of Mordred (evil)."

class Merlin(LoyalServantOfArthur):
    canSeeMinions = True
    visableToPercival = True
    help_text = "Merlin (good).\nKnows who are evil, must remain hidden.\nIf assissinated evil will win"

class Percival(LoyalServantOfArthur):
    help_text = "Percival (good).\nKnows Merlin"

class Assassin(MinionOfMordred):
    canAssassinate = True
    help_text = "Assassin (evil).\nAt the end of the game, gets to choose one player to assissinate.\n If that player is Merlin, evil wins the game"

class Mordred(MinionOfMordred):
    visableToMerlin = False
    help_text = "Mordred (evil).\nUnknown to Merlin"

class Morgana(MinionOfMordred):
    visableToPercival = True
    help_text = "Morgana (evil).\nAppears as Merlin to Percival"

class Oberon(MinionOfMordred):
    canSeeMinions = False
    help_text = "Oberon (evil).\nUnknown to Evil"
