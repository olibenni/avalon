bool_input = {"y": True, "n": False}

class Player:
    def __init__(self, name, card):
        self.name = name
        self.card = card

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def _get_input(self, text):
        text = self.name + ": " + text
        answer = None
        while answer is None:
            answer = bool_input.get(input(text))

        return answer


    def choose_team(self, players, quest):
        bool_input = {"y": True, "n": False}
        team = []
        i = 0
        while len(team) < quest.team_size:
            i = i % len(players)
            player = players[i]
            if player not in team:
                answer = self._get_input("Do you want {} on your team, (y/n)? ".format(player.name))
                if answer:
                    team.append(player)
            i += 1

        return team

    def vote_on_team(self, team):
        return self._get_input("Approve team {}, (y/n)? ".format(team))

    def choose_quest_card(self):
        answer = self._get_input("Do you want the Quest to succeed?, (y/n)? ")
        if answer is False and self.card.good:
            print("{} You are on the good team and therefor cannot choose to Fail the Quest".format(self))
            print("Overriding choice to Success")
            answer = True
        return answer