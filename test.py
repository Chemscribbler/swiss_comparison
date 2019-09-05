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


if __name__ == '__main__':
    unittest.main()
