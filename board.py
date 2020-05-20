class Board:
    quests = []
    number_of_minions_of_mordred = 0

    def __init__(self, number_of_players):
        if number_of_players == 5:
            self.number_of_minions_of_mordred = 2
            self.quests = [Quest(2), Quest(3), Quest(2), Quest(3), Quest(3)]
        elif number_of_players == 6:
            self.number_of_minions_of_mordred = 2
            self.quests = [Quest(2), Quest(3), Quest(4), Quest(3), Quest(4)]
        elif number_of_players == 7:
            self.number_of_minions_of_mordred = 3
            self.quests = [Quest(2), Quest(3), Quest(3), Quest(4, 2), Quest(4)]
        elif number_of_players in [8, 9]:
            self.number_of_minions_of_mordred = 3
            self.quests = [Quest(3), Quest(4), Quest(4), Quest(5, 2), Quest(5)]
        elif number_of_players == 10:
            self.number_of_minions_of_mordred = 4
            self.quests = [Quest(3), Quest(4), Quest(4), Quest(5, 2), Quest(5)]
        else:
            raise Exception("Only support 5-10 players")


class Quest:
    def __init__(self, team_size, number_of_fails_required = 1):
        self.team_size = team_size
        self.number_of_fails_required = number_of_fails_required
        self.vote_track = 1
