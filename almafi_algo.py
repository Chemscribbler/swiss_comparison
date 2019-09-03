import random


class Tournament:
    def __init__(self):
        self.playerlist = {}

    def add_player(self, name, id_corp, id_run):
        player = Player(name, id_corp, id_run)
        self.playerlist.update({player.id: player})

    def add_sim_player(self, name, id_corp, id_run, strength=0.5):
        sim = Sim(name, id_corp, id_run, strength)
        self.playerlist.update({sim.id: sim})

    def game_result(self, winner_id, loser_id):
        self.playerlist[winner_id].win(loser_id)
        self.playerlist[loser_id].lose(winner_id)

    def sim_game(self, sim1, sim2):
        rand = random.random()
        if rand + sim1.stength - sim2.strength > 0.5:
            self.game_result(sim1.id, sim2.id)
        else:
            self.game_result(sim2.id, sim1.id)

    def round_sos_calc(self):
        for player in self.playerlist:
            player.calc_sos()
        for player in self.playerlist:
            player.calc_ext_sos()

    def almafi_pairing(self):
        pass
    # TODO pair based on Almafi algorithm
        # Pairing is based on 1st should play the person below them equal to the number of rounds remaining
        # So in the first round of a 4 round tournament 1st plays 5th, 2nd plays 6th, etc.
        # In the second round 1st plays 4th, 2nd plays 5th, etc.
        # Third round 1st plays 3rd, 2nd plays 4th
        # Fourth round 1st plays 2nd

    def swiss_pairing(self):
        pass
    # TODO generate a standard swiss pairing algorithm

    def sim_round(self, pairing_func):
        pass
    # TODO generate a method to run a simmulated round, ideal functionality would allow counter-factual Swiss/Almafi


class Player(Tournament):
    next_id = 0

    def __init__(self, name, id_corp, id_run):
        super().__init__()
        self.id = Player.next_id
        Player.next_id += 1
        self.name = name
        self.id_corp = id_corp
        self.id_run = id_run
        self.score = 0
        self.sos = 0
        self.ext_SOS = 0
        self.opp_list = []

    def win(self, opponent_id):
        self.score += 3
        self.opp_list.append(opponent_id)

    def lose(self, opponent_id):
        self.opp_list.append(opponent_id)

    def calc_sos(self):
        self.sos = 0
        for opponent_id in self.opp_list:
            self.sos += self.playerlist[opponent_id].score
        self.sos = self.sos / len(self.opp_list)

    def calc_ext_sos(self):
        self.ext_SOS = 0
        for opponent_id in self.opp_list:
            self.sos += self.playerlist[opponent_id].SOS
        self.ext_SOS = self.ext_SOS/len(self.opp_list)


class Sim(Player):
    def __init__(self, name, corp_id, run_id, strength):
        super.__init__(name, corp_id, run_id)
        self.strength = strength
        self.sim = True
