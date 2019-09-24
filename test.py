import unittest

from almafi_algo import Player
from almafi_algo import Tournament
from almafi_algo import num_rounds


class TournamentTest(unittest.TestCase):
    def test_can_create_player(self):
        test_player = Player('a', 'b', 'c')

    def test_can_change_player_name(self):
        test_player = Player('a', 'b', 'c')
        self.assertEqual(test_player.name, 'a')

        test_player.name = 'b'
        self.assertNotEqual(test_player.name, 'a')
        self.assertEqual(test_player.name, 'b')


class AutoSimTesting(unittest.TestCase):
    # TODO write test to iterate over player counts & ensure opponents equal # of rounds*2
    # TODO write test to ensure number of rounds is appropriate

    def test_everyone_plays(self, player_count=24):
        test_tournament = Tournament()
        test_tournament.gen_sim_players(player_count)
        rounds = num_rounds(player_count)
        rounds_played = 0
        while rounds > 0:
            test_tournament.almafi_pairing(rounds)
            test_tournament.sim_round()
            rounds_played += 1
            for sim_player in test_tournament.rank_players():
                with self.subTest():
                    self.assertEqual(len(sim_player.opp_list), rounds_played*2)
            rounds -= 1

    def test_variable_player_counts(self):
        for i in range(8, 280):
            self.test_everyone_plays(i)





if __name__ == '__main__':
    unittest.main()
