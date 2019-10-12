from utility_functions import cut_size
from copy import deepcopy


class Player:
    next_id = 0

    def __init__(self, name, id_corp, id_run):
        self.id = Player.next_id
        Player.next_id += 1
        self.name = name
        self.id_corp = id_corp
        self.id_run = id_run
        self.score = 0
        self.sos = 0
        self.ext_sos = 0
        self.opp_list = []
        self.record = []
        self.curr_opp = None

    def win(self, opponent_id):
        self.score += 3
        self.opp_list.append(opponent_id)
        self.record.append("W")

    def lose(self, opponent_id):
        self.opp_list.append(opponent_id)
        self.record.append("L")

    def test_legal_pairing(self, opponent):
        if self.curr_opp is None and opponent.id not in self.opp_list:
            return True
        else:
            return False

    def compute_should_id(self, tournament, round_num):
        cut_count = cut_size(len(tournament.player_dict))
        made_cut = 0.0

        for i in range(0, 10000):
            drawn_scenario = deepcopy(tournament)
            clone = drawn_scenario.player_dict[self.id]
            temp_round = round_num
            while temp_round > 0:
                clone.draw_round(drawn_scenario)
                drawn_scenario.sim_round()
                temp_round -= 1
                drawn_scenario.almafi_pairing(temp_round)
            if clone.id in [player.id for player in drawn_scenario.cut(cut_count)]:
                made_cut += 1.0
            i += 1
        return made_cut/10000

    def draw_round(self, tournament):
        for pair in tournament.pairing_list:
            if self.id in pair:
                tournament.game_result(pair[0], pair[1])
                tournament.game_result(pair[1], pair[0])
                tournament.close_match(pair[0], pair[1])
                break


class Sim(Player):
    def __init__(self, name, corp_id, run_id, strength):
        super().__init__(name, corp_id, run_id)
        self.strength = strength
        self.sim = True
