#!/usr/bin/python3
"""Test User class"""

import unittest
from models.user import User
from models.feedback import Feedback
from models.schedule import Schedule
from models.route import Route
from models import storage
import hashlib


class TestUserClass(unittest.TestCase):

    def setUp(self):
        # Create a single User instance for each test
        self.user = User(email="test@example.com", password="password123", first_name="John", last_name="Doe")
        self.user.save()

    @classmethod
    def tearDownClass(cls):
        # Close the storage session after all tests
        storage.close()

    def test_user_attributes(self):
        retrieved_user = storage.get("User", self.user.id)
        pwd = "password123"
        self.assertEqual(retrieved_user.email, "test@example.com")
        self.assertEqual(retrieved_user.password, hashlib.md5(pwd.encode()).hexdigest())
        self.assertEqual(retrieved_user.first_name, "John")
        self.assertEqual(retrieved_user.last_name, "Doe")
        self.assertEqual(retrieved_user.feedbacks, [])

    def test_modify_user_attributes(self):
        # Modify user attributes
        modified_user = storage.get("User", self.user.id)
        modified_user.email = "modified@example.com"
        modified_user.save()

        # Ensure the modifications are saved
        retrieved_user = storage.get("User", self.user.id)

        self.assertEqual(retrieved_user.email, "modified@example.com")
    
    def test_invalid_user_email(self):
        with self.assertRaises(ValueError):
            invalid_user_email = storage.get("User", self.user.id)
            invalid_user_email.email = "modifiedexample.com"
            invalid_user_email.save()


    def test_relationship_between_user_and_one_feedback(self):
        # Create the a schedule and a route
        schedule = Schedule()
        schedule.save()

        route = Route(
            schedule_id=schedule.id,
            route_number=123,
            departure_terminus="terminus1",
            arrival_terminus="terminus2"
        )
        route.save()

        # Create the feedback
        feedback = Feedback(user_id=self.user.id, route_id=route.id, rating=5, comment="Great service!")
        feedback.save()

        # Get the user and the feedback
        retrieved_user = storage.get("User", self.user.id)
        retrieved_feedback = storage.get("Feedback", feedback.id)

        # Ensure the feedback is associated with the user
        self.assertEqual(retrieved_user.feedbacks, [retrieved_feedback])
        self.assertEqual(retrieved_feedback.user, retrieved_user)

    def test_relationship_between_user_and_two_feedbacks(self):
        # Create the a schedule and a route
        schedule = Schedule()
        schedule.save()

        route = Route(
            schedule_id=schedule.id,
            route_number=123,
            departure_terminus="terminus1",
            arrival_terminus="terminus2"
        )
        route.save()
        
        # Create the first feedback
        feedback1 = Feedback(user_id=self.user.id, route_id=route.id, rating=5, comment="Great service!")
        feedback1.save()

        # Create the second feedback
        feedback2 = Feedback(user_id=self.user.id, route_id=route.id, rating=4, comment="Good experience!")
        feedback2.save()

        # Get the user and the feedbacks
        retrieved_user = storage.get("User", self.user.id)
        retrieved_feedback1 = storage.get("Feedback", feedback1.id)
        retrieved_feedback2 = storage.get("Feedback", feedback2.id)

        # Ensure the feedbacks are associated with the user
        self.assertEqual(set(retrieved_user.feedbacks), {retrieved_feedback1, retrieved_feedback2})
        self.assertEqual(retrieved_feedback1.user, retrieved_user)
        self.assertEqual(retrieved_feedback2.user, retrieved_user)


if __name__ == '__main__':
    unittest.main()
