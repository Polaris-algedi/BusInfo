#!/usr/bin/python3
""" Test Route class """

import unittest
from models.route import Route
from models.schedule import Schedule
from models.feedback import Feedback
from models.user import User
from models.bus import Bus
from models.stop import BusStop

from models import storage



class TestRouteClass(unittest.TestCase):
    """ Test Route class """
    
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
    
    @classmethod
    def tearDownClass(cls):
        """ Close the storage session after all test """

        storage.close()

    def test_route_attributes(self):
        """ Test route attributes """
        retrieved_route = storage.get("Route", self.route.id)

        self.assertEqual(retrieved_route.schedule_id, self.schedule.id)
        self.assertIs(retrieved_route.schedule, self.schedule)
        self.assertEqual(retrieved_route.route_number, 123)
        self.assertEqual(retrieved_route.departure_terminus, "terminus1")
        self.assertEqual(retrieved_route.arrival_terminus, "terminus2")

        self.assertListEqual(retrieved_route.feedbacks, [])
        self.assertListEqual(retrieved_route.buses, [])
        self.assertListEqual(retrieved_route.stops, [])

    def test_route_relationship_with_feedbacks(self):
        """ Test the route relationship with Feedback class """
        user = User(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        user.save()

        feedback1 = Feedback(
            user_id=user.id,
            route_id=self.route.id,
            rating=5,
            comment="Great experience!"
        )
        feedback1.save()

        feedback2 = Feedback(
            user_id=user.id,
            route_id=self.route.id,
            rating=4,
            comment="Great experience!"
        )
        feedback2.save()

        retrieved_route = storage.get("Route", self.route.id)
        retrieved_feedback1 = storage.get("Feedback", feedback1.id)
        retrieved_feedback2 = storage.get("Feedback", feedback2.id)

        self.assertEqual(set(retrieved_route.feedbacks), {retrieved_feedback1, retrieved_feedback2})
        self.assertIs(retrieved_feedback1.route, retrieved_route)
        self.assertIs(retrieved_feedback2.route, retrieved_route)

    def test_route_relationship_with_buses(self):
        """ Test the route relationship with Bus class """

        bus1 = Bus(
            route_id=self.route.id,
            bus_number=1,
            capacity=50,
            current_location="stop1"
        )
        bus1.save()

        bus2 = Bus(
            route_id=self.route.id,
            bus_number=2,
            capacity=50,
            current_location="stop2"
        )
        bus2.save()

        retrieved_route = storage.get("Route", self.route.id)
        retrieved_bus1 = storage.get("Bus", bus1.id)
        retrieved_bus2 = storage.get("Bus", bus2.id)

        self.assertEqual(set(retrieved_route.buses), {retrieved_bus1, retrieved_bus2})
        self.assertIs(retrieved_bus1.route, retrieved_route)
        self.assertIs(retrieved_bus2.route, retrieved_route)

    def test_route_relationship_with_stops(self):
        """ Test the route relationship with BusStop class """

        stop1 = BusStop(
            route_id=self.route.id,
            stop_name="Aya 1",
            place="Zan9a 50",
            is_terminus=False
        )
        stop1.save()

        stop2 = BusStop(
            route_id=self.route.id,
            stop_name="Aya 2",
            place="Zan9a 50",
            is_terminus=True
        )
        stop2.save()

        retrieved_route = storage.get("Route", self.route.id)
        retrieved_stop1 = storage.get("BusStop", stop1.id)
        retrieved_stop2 = storage.get("BusStop", stop2.id)

        self.assertEqual(set(retrieved_route.stops), {retrieved_stop1, retrieved_stop2})
        self.assertIs(retrieved_stop1.route, retrieved_route)
        self.assertIs(retrieved_stop2.route, retrieved_route)

    

if __name__ == '__main__':
    unittest.main()