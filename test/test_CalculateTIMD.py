import unittest

from calculations import calculateTIMD


class TestCalculateTIMD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compressed_timd = 'A52B2500CaDaEcFtGfHkImJt|KrLyM146NmOvPf,KqLpM144Nl,KrLyM143NlOvPt,KqLpM139Nl,KrLyM137NlOvPf,KqLpM135Nl,KrLyM134NlOvPf,KqLpM132Nl,KrLyM130NlOuPf,KqLoM128Nl,KrLyM126NlOuPf,KqLpM124Nl,KrLyM123NlOuPt,KqLoM121Nl,KrLyM119NlOuPt,KqLoM117Nl,KrLyM115NlOsPf,KqLoM113Nl,KrLyM112NlOsPf,KqLoM110Nl,KrLyM109NlOsPt,KqLoM107Nl,KrLyM106NlOsPt,KqLoM103Nm,KrLyM102NmOvPf,KqLoM99Nm,KrLyM98NmOvPf,KqLpM97Nm,KrLyM95NmOvPt,KqLpM93Nm,KrLyM92NmOvPt,KqLpM90Nm,KrLyM89NmOuPt,KqLpM87Nm,KrLyM86NmOuPt,KqLpM84Nm,KrLyM82NmOuPt,KqLpM80Nm,KrLyM78NmOsPt,KqLpM77Nm,KrLyM75NmOsPt,KqLpM74Nm,KrLyM72NmOsPf,KqLpM71Nm,KrLyM70NmOsPf,KqLpM68Nm,KrLzM66NmOsQwPt,KqLoM62Nm,KrLzM60NmOsQwPt,KqLpM57Nm,KrLzM56NmOsQxPt,KqLpM53Nm,KrLzM51NmOsQxPt,KqLpM47Nm,KrLyM44NmOuPf,KqLpM42Nl,KrLzM41NlOsQwPf,KqLpM38Nl,KrLzM37NlOsQwPf,KqLpM35Nl,KrLzM34NlOsQxPt,KqLpM32Nl,KrLzM30NlOsQxPf,KqLpM28Nl,KrLzM27NlOsQxPt,KqLpM25Nm,KrLzM23NmOsQxPt,KqLpM22Nm,KrLzM20NmOsQxPt,KagM17,KafM16,KacM15,KadM14,KagM14,KacM13,KacM12,KafM11,KaeM9RvSvUtVt'
        cls.timd_name = 'QM52-2500-a'
        cls.timd = calculateTIMD.calculate_timd(cls.compressed_timd, cls.timd_name, test=True)

    def testCalculatePlacements(self):
        self.assertEqual(self.timd['calculated']['cargoScored'], 16)

    def testCalculateDrops(self):
        self.assertEqual(self.timd['calculated']['cargoDropped'], 0)

    def testCalculateTeleop(self):
        self.assertEqual(self.timd['calculated']['hatchScoredTeleop'], 18)

    def testScoredLevel3(self):
        self.assertEqual(self.timd['calculated']['hatchScoredLevel3'], 5)

    def testScoredRocket(self):
        self.assertEqual(self.timd['calculated']['hatchScoredRocket'], 13)

    def testPlacementPercentage(self):
        self.assertEqual(self.timd['calculated']['cargoPlaceSuccessRate'], 100)

    def testTrueOffensiveContribution(self):
        self.assertEqual(self.timd['calculated']['trueOffensiveContribution'], 95)

    def testUndefendedHatchCycleTimes(self):
        self.assertEqual(self.timd['calculated']['undefendedHatchAverageCycleTime'], 1.6)

    def testUndefendedRocketAverageCycleTime(self):
        self.assertEqual(self.timd['calculated']['undefendedRocketAverageCycleTime'], 1.6)

    def testUndefendedLevel3AverageCycleTime(self):
        self.assertEqual(self.timd['calculated']['undefendedLevel3AverageCycleTime'], 1.2)

    def testDefendedCargoAverageCycleTime(self):
        self.assertEqual(self.timd['calculated']['defendedCargoAverageCycleTime'], 1.1)

    def testDefendedCargoShipAverageCycleTime(self):
        self.assertEqual(self.timd['calculated']['defendedCargoShipAverageCycleTime'], 1.6)

    def testDefendedLevel3AverageCycleTime(self):
        self.assertEqual(self.timd['calculated']['defendedLevel3AverageCycleTime'], 1.3)

    def testTimeClimbing(self):
        self.assertEqual(self.timd['calculated']['timeClimbing'], 9)

    def testTimeIncap(self):
        self.assertEqual(self.timd['calculated']['timeIncap'], 2)

    def testTimeDefending(self):
        self.assertEqual(self.timd['calculated']['timeDefending'], 4)


if __name__ == '__main__':
    unittest.main()
