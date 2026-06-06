import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.io import DatabaseReader
from src.core import TaRFM

class TestTaRFMPhases(unittest.TestCase):
    
    def setUp(self):
        self.reader = DatabaseReader()
        self.tx_file = "data/sample/transactions.txt"
        self.util_file = "data/sample/external_utility.txt"
        
    def test_end_to_end_accuracy(self):
        database = self.reader.read(self.tx_file, self.util_file)
        tarfm = TaRFM()
        
        qi_set = {"A", "B"}
        delta = 0.01
        gamma = 1.5
        alpha = 0.2
        beta = 80.0
        
        patterns = tarfm.run(database, qi_set, delta, gamma, alpha, beta)
        
        # Chúng ta mong đợi 2 patterns: {A, B} và {A, B, F}
        self.assertEqual(len(patterns), 2)
        
        pattern_abf = next((p for p in patterns if "F" in p.get_items()), None)
        self.assertIsNotNone(pattern_abf)
        self.assertEqual(pattern_abf.get_frequency(), 2)
        self.assertAlmostEqual(pattern_abf.get_monetary(), 476.0, places=2)
        self.assertAlmostEqual(pattern_abf.get_recency(), 1.837, places=2)

if __name__ == '__main__':
    unittest.main()
