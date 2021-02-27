import random
from board import Board
import card
from player import Player

vote_to_string = {True: "Yes", False: "No"}

class Game:
    current_king = None
    board = None
    players = []
    over = False
    wins = []

    def _include_card(self, card):
        bool_input = {"y": True, "n": False, "help": "help"}
        answer = None
        while answer is None:
            answer = bool_input.get(input("Include {} (y/n/help)? ".format(card)))
            if answer == "help":
                print("================")
                print(card.help_text)
                print("================")
                answer = None

        return card if answer else False

    def _choose_minions(self, include_percival):
        include_morgana = False
        if include_percival:
            include_morgana = self._include_card(card.Morgana())
        include_mordred = self._include_card(card.Mordred())
        include_oberon = self._include_card(card.Oberon())
        # We always include Assassin
        return [card for card in [card.Assassin(), include_morgana, include_mordred, include_oberon] if card]

    def start(self):
        number_of_players = "0"
        while number_of_players not in [str(i) for i in range(5, 11)]:
            number_of_players = input("How many players (5-10)?: ")

        number_of_players = int(number_of_players)
        board = Board(number_of_players)

        include_percival = self._include_card(card.Percival())

        included_servants = [card.Merlin()] + ([include_percival] if include_percival else [])
        included_minions = self._choose_minions(include_percival)

        while board.number_of_minions_of_mordred < len(included_minions):
            print("Too many minions of Mordred included!\nIn a {} player game there are only {} minions and you included {}".format(number_of_players, board.number_of_minions_of_mordred, len(included_minions)))
            print("Included minions: {}".format(", ".join([str(card) for card in included_minions])))
            included_minions = self._choose_minions(include_percival)

        for i in range(board.number_of_minions_of_mordred - len(included_minions)):
            included_minions.append(card.MinionOfMordred())

        for i in range(number_of_players - board.number_of_minions_of_mordred - len(included_servants)):
            included_servants.append(card.LoyalServantOfArthur())

        deck = included_minions + included_servants
        print(deck)
        random.shuffle(deck)
        print(deck)

        for i in range(number_of_players):
            name = input("Name for player {}: ".format(i + 1))
            self.players.append(Player(name, deck.pop()))
        for player in self.players:
            player.card.explain_role(self.players)

        self.board = board

    def next_turn(self):
        self.next_king()
        print("King is: {}".format(self.current_king))
        print("Current Quest results {}".format(self.wins))

        quest_number = len(self.wins)
        quest = self.board.quests[quest_number]
        print("Current Quest number {}. The Quest requires {} Fail(s) in order to fail".format(quest_number + 1, quest.number_of_fails_required))

        team = self.current_king.choose_team(self.players, quest)
        votes = []
        for player in self.players:
            votes.append(player.vote_on_team(team))
        for player_vote in zip(self.players, votes):
            print("{} voted {}".format(player_vote[0], vote_to_string[player_vote[1]]))
        if sum(votes) > len(self.players) // 2:
            print("Team is approved by majority vote")
            quest_cards = []
            for player in team:
                quest_cards.append(player.choose_quest_card())
            random.shuffle(quest_cards)
            print("Votes are in! {}".format(quest_cards))
            res = quest_cards.count(False) < quest.number_of_fails_required
            if res:
                print("The Quest is successful!")
            else:
                print("The Quest failed....")
            self.wins.append(res)
            if sum(self.wins) == 3 or self.wins.count(False) == 3:
                game.over = True
        else:
            quest.vote_track += 1
            print("Team is not approved. Moving vote track to {}".format(quest.vote_track))
            if quest.vote_track == 5:
                game.over = True


    def next_king(self):
        if self.current_king is None:
            self.current_king = self.players[0]
        else:
            count = 0
            for player in self.players:
                count += 1
                if player == self.current_king:
                    if len(self.players) == count:
                        self.current_king = self.players[0]
                    else:
                        self.current_king = self.players[count]
                    return

    def attempt_merlin_assassination(self):
        for player in self.players:
            if type(player.card) == card.Assassin:
                victim = player.attempt_merlin_assassination(self.players)
                print("{} assassinated {} who is {}".format(player, victim, victim.card))
                return type(victim.card) == card.Merlin


if __name__ == "__main__":
    game = Game()
    game.start()
    while not game.over:
        game.next_turn()
    print("GAME OVER")
    if sum(game.wins) == 3:
        if game.attempt_merlin_assassination():
            print("Evil wins via assassination of Merlin")
        else:
            print("Good wins!")
    else:
        print("Evil wins!")