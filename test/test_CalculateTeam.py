import unittest
import json
import os

from calculations import calculateTeam


class TestCalculateTeam(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        f = open(os.path.join(os.getcwd(), "1816.json"))
        cls.team = json.loads(f.read())
        f.close()
        cls.team = calculateTeam.calculate_team(1816, 0, cls.team)

    def testLoadedCorrectly(self):
        self.assertEqual(self.team['teamNumber'], 1816)

    def testTeamAbilitesIntake(self):
        self.assertEqual(self.team['team_abilities']['groundCargoPickup'], True)

    def testTeamAbilitesSandstorm(self):
        self.assertEqual(self.team['team_abilities']['startLevel2'], True)

    def testTeamAbilitesPlace(self):
        self.assertEqual(self.team['team_abilities']['placeLevel3'], False)

    def testTeamAbilitesClimb(self):
        self.assertEqual(self.team['team_abilities']['climbHab3'], True)

    def testTotalsTimeline(self):
        self.assertEqual(self.team['totals']['cargoPlaced'], 9)

    def testTotalsAveragesTimeline(self):
        self.assertEqual(self.team['totals']['avgCargoScoredL1'], 1.1)

    def testL3MsAveragesTimeline(self):
        self.assertEqual(self.team['l3ms']['l3mHatchesScoredL1'], 1.7)

    def testp75sTimeline(self):
        self.assertEqual(self.team['p75s']['p75CargoScored'], 2.2)

    def testSDTimeline(self):
        self.assertEqual(self.team['SDs']['SDCargoScored'], 1.3)

    def testMaxesTimeline(self):
        self.assertEqual(self.team['maxes']['maxCargoScored'], 3)
