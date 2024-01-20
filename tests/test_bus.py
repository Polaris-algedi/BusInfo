#!/usr/bin/python3
"""Test Bus class"""

import unittest
from models.schedule import Schedule
from models.route import Route
from models.bus import Bus
from models import storage

class TestBusClass(unittest.TestCase):

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

        self.bus = Bus(
            route_id=self.route.id,
            bus_number=1,
            capacity=50,
            current_location="stop1"
        )
        self.bus.save()

    @classmethod
    def tearDownClass(cls):
        # Close the storage session after all tests
        storage.close()

    def test_bus_attributes_and_relationships(self):
        # Retrieve the bus from the database
        retrieved_bus = storage.get("Bus", self.bus.id)

        # Check if attributes match the values set in setUp
        self.assertEqual(retrieved_bus.route_id, self.route.id)
        self.assertEqual(retrieved_bus.bus_number, 1)
        self.assertEqual(retrieved_bus.capacity, 50)
        self.assertEqual(retrieved_bus.current_location, "stop1")

        # Check if relationships are correctly set
        self.assertIs(retrieved_bus.route, self.route)
        self.assertIn(retrieved_bus, self.route.buses)


if __name__ == '__main__':
    unittest.main()