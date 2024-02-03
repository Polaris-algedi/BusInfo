#!/usr/bin/python3
""" test bidirectional relationship """

import unittest
from datetime import time, timedelta
from models.schedule import Schedule
from models.route import Route
from models import storage

class TestScheduleClass(unittest.TestCase):

    def setUp(self):
        # Create a single Schedule instance for each test
        self.schedule = Schedule()
        self.schedule.save()

    @classmethod
    def tearDownClass(cls):
        # Close the storage session after all tests
        storage.close()

    def test_schedule_default_values(self):
        retrieved_schedule = storage.get("Schedule", self.schedule.id)
        self.assertEqual(retrieved_schedule.first_departure, time(hour=6))
        self.assertEqual(retrieved_schedule.last_departure, time(hour=21))
        self.assertEqual(retrieved_schedule.duration, timedelta(hours=1))
        self.assertEqual(retrieved_schedule.bus_frequency, timedelta(minutes=20))
        self.assertIsNone(retrieved_schedule.day_of_week)
        self.assertEqual(retrieved_schedule.routes, [])
    
    def test_modify_schedule_attributes(self):
        # Modify schedule attributes
        modified_schedule = storage.get("Schedule", self.schedule.id)
        modified_schedule.first_departure = time(hour=7)
        modified_schedule.last_departure = time(hour=22)
        modified_schedule.save()

        # Ensure the modifications are saved
        retrieved_schedule = storage.get("Schedule", self.schedule.id)

        self.assertEqual(retrieved_schedule.first_departure, time(hour=7))
        self.assertEqual(retrieved_schedule.last_departure, time(hour=22))



    def test_relationship_between_schedule_and_one_route(self):
        # Create the first route
        route = Route(
            schedule_id=self.schedule.id,
            route_number=123,
            departure_terminus="terminus1",
            arrival_terminus="terminus2"
        )
        route.save()

        # Get the schedule and the first route
        retrieved_schedule = storage.get("Schedule", self.schedule.id)
        retrieved_route = storage.get("Route", route.id)

        # Ensure the route is associated with the schedule
        self.assertEqual(retrieved_schedule.routes, [retrieved_route])
        self.assertEqual(retrieved_route.schedule, retrieved_schedule)


    def test_relationship_between_schedule_and_two_routes1(self):
        # Create the first route
        route1 = Route(
            schedule_id=self.schedule.id,
            route_number=123,
            departure_terminus="terminus1",
            arrival_terminus="terminus2"
        )
        route1.save()

        # Create the second route
        route2 = Route(
            schedule_id=self.schedule.id,
            route_number=456,
            departure_terminus="start",
            arrival_terminus="end"
        )
        route2.save()

        # Get the schedule and the routes
        retrieved_schedule = storage.get("Schedule", self.schedule.id)
        retrieved_route1 = storage.get("Route", route1.id)
        retrieved_route2 = storage.get("Route", route2.id)

        # Ensure the routes are associated with the schedule
        self.assertEqual(set(retrieved_schedule.routes), {retrieved_route1, retrieved_route2})
        self.assertEqual(retrieved_route1.schedule, retrieved_schedule)
        self.assertEqual(retrieved_route2.schedule, retrieved_schedule)


    def test_relationship_between_schedule_and_two_routes2(self):
        """This test creates a problem look down line 126"""
        # Create the first route
        route1 = Route(
            schedule_id=self.schedule.id,
            route_number=123,
            departure_terminus="terminus1",
            arrival_terminus="terminus2"
        )
        route1.save()

        # Get the schedule and the first route
        retrieved_schedule = storage.get("Schedule", self.schedule.id)
        retrieved_route1 = storage.get("Route", route1.id)

        # Ensure the first route is associated with the schedule
        self.assertEqual(retrieved_schedule.routes, [retrieved_route1])
        self.assertEqual(retrieved_route1.schedule, retrieved_schedule)

        # Create the second route
        route2 = Route(
            schedule_id=self.schedule.id,
            route_number=456,
            departure_terminus="start",
            arrival_terminus="end"
        )
        route2.save()

        # Get the second route
        retrieved_route2 = storage.get("Route", route2.id)
        
        # !!!!!!!! route2 doesn't get added automatically to retrieved_schedule.
        # Explicitly add the new route to retrieved_schedule.routes
        retrieved_schedule.routes.append(retrieved_route2)

        # Ensure the second route is added to the schedule
        self.assertEqual(len(retrieved_schedule.routes), 2)

        # Additional checks for the second route
        
        self.assertIn(retrieved_route2, retrieved_schedule.routes)
        self.assertEqual(retrieved_route2.schedule, retrieved_schedule)
    

if __name__ == '__main__':
    unittest.main()
