from unittest import TestCase
from scoring import BinaryCategoryAggregator

class TestBinaryCategoryAggregator(TestCase):
    
    def setUp(self):
        self.agg = BinaryCategoryAggregator(10)  # point_value of 10
        
    def test01(self):
        """No translations"""
        self.assertEqual(self.agg(0, 0, 0), 0)
        self.assertEqual(self.agg(0, 0, 1), 10)
        self.assertEqual(self.agg(0, 1, 0), 10)
        self.assertEqual(self.agg(0, 1, 1), 5)
        self.assertEqual(self.agg(1, 0, 0), 10)
        self.assertEqual(self.agg(1, 0, 1), 2.5)
        self.assertEqual(self.agg(1, 1, 0), 2.5)
        self.assertEqual(self.agg(1, 1, 1), 0)

    def test02(self):
        """With ranslations"""
        self.assertEqual(self.agg('no', 0, 0), 0)
        self.assertEqual(self.agg(0, 'no', 'yes'), 10)
        self.assertEqual(self.agg(0, 'true', 'false'), 10)
        self.assertEqual(self.agg(False, True, 1), 5)
        self.assertEqual(self.agg(True, 'false', 'no'), 10)

