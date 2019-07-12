import pytest
import unittest
from src.backend.Request import Request


class RequestTest(unittest.TestCase):
    def test_get_hotels(self):
        req = Request(current_city='Chicago', travel_city='Los Angeles', num_people='2', st_date='2019-04-10',
                      end_date='2019-04-15', ratings='5,4,3,2', max_fbudget='300')
        json = req.get_hotels()
        self.assertEqual(len(json), 2)
        self.assertEqual(json[0]['hotel']['chainCode'], 'RD')
        self.assertEqual(json[0]['hotel']['cityCode'], 'LAX')

        req = Request(current_city='Chicago', travel_city='Knoxville', num_people='2', st_date='2019-04-10',
                      end_date='2019-04-15', ratings='5,4,3,2', max_fbudget='300')

        json = req.get_hotels()
        self.assertEqual(len(json), 25)
        self.assertEqual(json[0]['hotel']['chainCode'], 'HX')
        self.assertEqual(json[0]['hotel']['cityCode'], 'TYS')

    def test_get_flights(self):
        req = Request(current_city='Chicago', travel_city='Knoxville', num_people='2', st_date='2019-04-10',
                      end_date='2019-04-15', ratings='5,4,3,2', max_fbudget=500)

        json = req.get_flight()
        self.assertEqual(json[0]['id'], '1550981718711-1240260075')

    def test_get_airports(self):
        req = Request(current_city='Chicago', travel_city='Knoxville', num_people='2', st_date='2019-04-10',
                      end_date='2019-04-15', ratings='5,4,3,2', max_fbudget=500)

        self.assertEqual(req.get_nearby_airports(), ['ORD', 'MDW', 'DTW', 'MKE', 'STL', 'IND', 'CVG', 'CLE', 'CMH', 'GRR'])

