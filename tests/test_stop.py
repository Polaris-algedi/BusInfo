#!/usr/bin/python3
"""Test Stop class"""

import unittest
from models.schedule import Schedule
from models.route import Route
from models.stop import BusStop
from models import storage

class TestStopClass(unittest.TestCase):

    def setUp(self):
        """ Create instances of related Classes for each test """

        self.schedule = Schedule()
        self.schedule.save()

        self.route = Route(
            schedule_id=self.schedule.id,
            route_number=123,
            departure_terminus="terminus1",
            arrival_terminus="terminus2"
        )
        self.route.save()

        self.stop = BusStop(
            route_id=self.route.id,
            stop_name="Aya 1",
            place="Zan9a 50",
            is_terminus=False
        )
        self.stop.save()

    @classmethod
    def tearDownClass(cls):
        # Close the storage session after all tests
        storage.close()

    def test_stop_attributes_and_relationships(self):
        """ Test stop attributes and relationships """
        
        # Retrieve the stop from the database
        retrieved_stop = storage.get("BusStop", self.stop.id)

        # Check if attributes match the values set in setUp
        self.assertEqual(retrieved_stop.route_id, self.route.id)
        self.assertEqual(retrieved_stop.stop_name, "Aya 1")
        self.assertEqual(retrieved_stop.place, "Zan9a 50")
        self.assertEqual(retrieved_stop.is_terminus, False)

        # Check if relationships are correctly set
        self.assertIs(retrieved_stop.route, self.route)
        self.assertIn(retrieved_stop, self.route.stops)


if __name__ == '__main__':
    unittest.main()