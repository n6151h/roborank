from unittest import TestCase
from scoring import BinaryCategoryAggregator

class TestBinaryCategoryAggregator(TestCase):
    
    def setUp(self):
        self.agg = BinaryCategoryAggregator(10)  # point_value of 10
        
    def test01(self):
        
        self.assertEqual(self.agg(0, 0, 0), 0)
        self.assertEqual(self.agg(0, 0, 1), 10)
        self.assertEqual(self.agg(0, 1, 0), 10)
        self.assertEqual(self.agg(0, 1, 1), 5)
        self.assertEqual(self.agg(1, 0, 0), 10)
        self.assertEqual(self.agg(1, 0, 1), 2.5)
        self.assertEqual(self.agg(1, 1, 0), 2.5)
        self.assertEqual(self.agg(1, 1, 1), 0)
