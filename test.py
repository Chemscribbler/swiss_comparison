import unittest

from almafi_algo import Player


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

    def test_everyone_plays(self):
        pass


if __name__ == '__main__':
    unittest.main()
