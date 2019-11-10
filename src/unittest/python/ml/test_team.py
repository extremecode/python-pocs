from unittest import TestCase
import unittest

from ml.team import Team

class TestTeam(TestCase):
    def test_team_features(self):
        justice_league_fav = Team(["batman", "wonder woman", "flash"])

        self.assertEqual(3,len(justice_league_fav))
        self.assertTrue("batman" in justice_league_fav)
        self.assertFalse("superman" in justice_league_fav)
        self.assertTrue("cyborg" not in justice_league_fav)

if __name__ == '__main__':
    unittest.main()

