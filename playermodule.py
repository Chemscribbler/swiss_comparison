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


class Sim(Player):
    def __init__(self, name, corp_id, run_id, strength):
        super().__init__(name, corp_id, run_id)
        self.strength = strength
        self.sim = True