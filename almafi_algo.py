import playermodule
import random
from operator import attrgetter

CORP_ID = ["Argus", "Blue Sun", "Gagarin", "GRNDL", 'Jemison',
           'Acme', 'Azmari', 'Haarpsichord', 'Harischandra', 'CtM',
           'AgInf', "Harmony Medtech", 'IG', "Biotech", "PE",
           "Asa", "CI", 'Custom Bio', 'CyDiv', 'AoT']

RUNNER_ID = ["Alice", "Ed", "Freedom", "MaxX", "Gnat",
             "419", "Andy", "Geist", "Az", "Gabe",
             "Akiko", "Ayla", "CT", "Smoke", "Exile",
             "Apex", "Adam", "Sunny"]


def is_legal_pair(player1, player2):
    return player1.test_legal_pairing(player2) and \
        player2.test_legal_pairing(player1)


def num_rounds(player_count, event_type="Competitive"):
    rounds = 3
    if event_type == "Competitive":
        if player_count > 9:
            rounds += 1
            if player_count > 32:
                rounds += 1
                if player_count > 56:
                    rounds += 1
                    if player_count > 80:
                        rounds += 1
                        if player_count > 128:
                            rounds += 1
                            if player_count > 192:
                                rounds += 1
                                if player_count > 256:
                                    rounds += 1
    if event_type == "Casual":
        if player_count > 11:
            rounds += 1
            if player_count > 15:
                rounds += 1
                if player_count > 32:
                    rounds += 1
                    if player_count > 64:
                        rounds += 1
                        if player_count > 96:
                            rounds += 1
                            if player_count > 128:
                                rounds += 1
    return rounds


class Tournament:
    def __init__(self):
        self.player_dict = {}
        self.pairing_list = []

    def add_player(self, name, id_corp, id_run):
        player = playermodule.Player(name, id_corp, id_run)
        self.player_dict.update({player.id: player})

    def add_sim_player(self, name, id_corp, id_run, strength=0.5):
        sim = playermodule.Sim(name, id_corp, id_run, strength)
        self.player_dict.update({sim.id: sim})

    def gen_sim_players(self, number):
        for i in range(0, number):
            corp_num = random.randint(0, 19)
            runner_num = random.randint(0, 17)
            self.add_sim_player(chr(65+i), CORP_ID[corp_num], RUNNER_ID[runner_num], random.random())

    def game_result(self, winner_id, loser_id):
        self.player_dict[winner_id].win(loser_id)
        self.player_dict[loser_id].lose(winner_id)

    def close_match(self, player1, player2):
        player1.curr_opp = None
        player2.curr_opp = None
        new_pairing_list = []
        for pair in self.pairing_list:
            if player1.id != pair[0].id:
                new_pairing_list.append(pair)
        self.pairing_list = new_pairing_list

    def sim_game(self, sim1, sim2):
        rand = random.random()
        if rand + sim1.strength - sim2.strength > 0.5:
            self.game_result(sim1.id, sim2.id)
        else:
            self.game_result(sim2.id, sim1.id)

    def round_sos_calc(self):
        for i in self.player_dict:
            sos = 0
            player = self.player_dict[i]
            for opp in player.opp_list:
                sos += self.player_dict[opp].score
            player.sos = sos/len(player.opp_list)
        for i in self.player_dict:
            ext_sos = 0
            player = self.player_dict[i]
            for opp in player.opp_list:
                ext_sos += self.player_dict[opp].sos
            player.ext_sos = ext_sos/len(player.opp_list)

    def rank_players(self):
        player_list = []
        for player in self.player_dict:
            player_list.append(self.player_dict[player])
        player_list.sort(key=attrgetter("ext_sos"))
        player_list.sort(key=attrgetter("sos"))
        player_list.sort(key=attrgetter("score"))
        return player_list

    def almafi_pairing(self, rounds_remaining):
        ranking = self.rank_players()
        self.pairing_list = []

        for playerRank in range(0, len(ranking)):
            player = ranking[playerRank]
            if player.curr_opp is None:
                # checks for valid match with players going down starting with player's position + rounds remaining
                for i in range(rounds_remaining+playerRank, len(ranking)):
                    if is_legal_pair(player, ranking[i]):
                        self.manage_pairing(player, ranking[i])
                        break
                    else:
                        i += 1
                # If no lower opponent could be found want to find check list for a higher ranked option
                if player.curr_opp is None:
                    for i in range(0, playerRank + rounds_remaining - 1):
                        # Want to start low, so invert the number
                        check = playerRank - rounds_remaining - i
                        if check <= len(ranking) and check != playerRank:
                            if is_legal_pair(player, ranking[check]):
                                self.manage_pairing(player, ranking[check])
                                break
                            else:
                                i += 1
                        else:
                            i += 1
                # TODO properly implement the bye as an opponent
                # if no legal opponent, set to -1, the bye
                if player.curr_opp is None:
                    player.curr_opp = -1

    def manage_pairing(self, player1, player2):
        self.pairing_list.append((player1, player2))
        player1.curr_opp = player2.id
        player2.curr_opp = player1.id

    def swiss_pairing(self):
        pass
    # TODO generate a standard swiss pairing algorithm

    def sim_round(self):
        for pair in self.pairing_list:
            self.sim_game(pair[0], pair[1])
            self.sim_game(pair[0], pair[1])
            self.close_match(pair[0], pair[1])
        self.round_sos_calc()

    def cut(self, number):
        return self.rank_players()[-number:]


# TODO find bug where not everyone is playing the same number of opponents (also implement unit test)
def run_sim_tournament(player_count, **kwargs):
    tournament = Tournament()
    rounds = num_rounds(player_count, **kwargs)
    tournament.gen_sim_players(player_count)
    while rounds > 0:
        tournament.almafi_pairing(rounds)
        tournament.sim_round()
        rounds -= 1
    return tournament
