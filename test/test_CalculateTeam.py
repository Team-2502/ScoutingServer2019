import unittest
import json
import os

from calculations import calculateTeam


class TestCalculateTeam(unittest.TestCase):
    def setUp(self):
        f = open(os.path.join(os.getcwd(), "1816.json"))
        self.team = json.loads(f.read())
        f.close()
        self.timd = calculateTeam.calculate_team(1816, 0, self.team)

    def testLoadedCorrectly(self):
        self.assertEqual(self.team['teamNumber'], 1816)
