import playermodule
import random
import utility_functions
from operator import attrgetter

CORP_ID = ["Argus", "Blue Sun", "Gagarin", "GRNDL", 'Jemison',
           'Acme', 'Azmari', 'Haarpsichord', 'Harischandra', 'CtM',
           'AgInf', "Harmony Medtech", 'IG', "Biotech", "PE",
           "Asa", "CI", 'Custom Bio', 'CyDiv', 'AoT']

RUNNER_ID = ["Alice", "Ed", "Freedom", "MaxX", "Gnat",
             "419", "Andy", "Geist", "Az", "Gabe",
             "Akiko", "Ayla", "CT", "Smoke", "Exile",
             "Apex", "Adam", "Sunny"]


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
            self.add_sim_player(chr(65+i), CORP_ID[corp_num], RUNNER_ID[runner_num], random.normalvariate(0.5, 0.2))

    def game_result(self, winner_id, loser_id):
        if loser_id > 0:
            self.player_dict[loser_id].lose(winner_id)
        self.player_dict[winner_id].win(loser_id)

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

        # If opponent is bye
        if sim1.id < 0:
            self.game_result(sim2.id, sim1.id)
        elif sim2.id < 0:
            self.game_result(sim1.id, sim2.id)

        # Coin flip result (strength1 - strength2)+random then if greater/less than 0.5
        elif rand + sim1.strength - sim2.strength > 0.5:
            self.game_result(sim1.id, sim2.id)
        else:
            self.game_result(sim2.id, sim1.id)

    def round_sos_calc(self):
        for i in self.player_dict:
            sos = 0
            player = self.player_dict[i]
            distinct_opp_list = []
            for x in player.opp_list:
                if x not in distinct_opp_list:
                    distinct_opp_list.append(x)
            for opp in distinct_opp_list:
                opp_obj = self.player_dict[opp]
                sos += opp_obj.score
            player.sos = round(sos/len(player.opp_list)/2, 3)
        for i in self.player_dict:
            ext_sos = 0
            player = self.player_dict[i]
            for opp in player.opp_list:
                ext_sos += self.player_dict[opp].sos
            player.ext_sos = round(ext_sos/len(player.opp_list), 3)

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

        if rounds_remaining < 1:
            return None

        for playerRank in range(0, len(ranking)):
            player = ranking[playerRank]
            if player.curr_opp is None:
                # checks for valid match with players going down starting with player's position + rounds remaining
                for i in range(rounds_remaining+playerRank, len(ranking)):
                    if utility_functions.is_legal_pair(player, ranking[i]):
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
                            if utility_functions.is_legal_pair(player, ranking[check]):
                                self.manage_pairing(player, ranking[check])
                                break
                            else:
                                i += 1
                        else:
                            i += 1
                # TODO implement un-pairing so that number of byes is minimized
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

    def check_id_prob(self, rounds_remaining):
        for p in self.rank_players():
            print("ID: {} Str: {} Score: {} SoS: {} Draw Odds: {}".format(p.id,
                  round(p.strength, 3), p.score, p.sos, p.compute_should_id(self, rounds_remaining)))

    def check_offers(self, rounds_remaining, **kwargs):
        for pair in self.pairing_list:
            p1_desire = pair[0].compute_should_id(self, rounds_remaining, **kwargs)
            p2_desire = pair[1].compute_should_id(self, rounds_remaining, **kwargs)
            if p1_desire > 0.85:
                print("{} offers draw to {}".format(pair[0].id, pair[1].id))
            if p2_desire > 0.85:
                print("{} would accept draw from {}".format(pair[1].id, pair[0].id))
        print("All offers completed")
