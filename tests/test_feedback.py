#!/usr/bin/python3
"""Test Feedback class"""

import unittest
from models.feedback import Feedback
from models.schedule import Schedule
from models.route import Route
from models.user import User
from models import storage

class TestFeedbackClass(unittest.TestCase):

    def setUp(self):
        # Create instances of related classes
        self.user = User(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.user.save()

        self.schedule = Schedule()
        self.schedule.save()
        
        self.route = Route(
            schedule_id=self.schedule.id,
            route_number=123,
            departure_terminus="terminus1",
            arrival_terminus="terminus2"
        )
        self.route.save()

        # Create a Feedback instance for each test
        self.feedback = Feedback(
            user_id=self.user.id,
            route_id=self.route.id,
            rating=5,
            comment="Great experience!"
        )
        self.feedback.save()

    @classmethod
    def tearDownClass(cls):
        # Close the storage session after all tests
        storage.close()

    def test_feedback_attributes_and_relationships(self):
        # Retrieve the feedback from the database
        retrieved_feedback = storage.get("Feedback", self.feedback.id)

        # Check if attributes match the values set in setUp
        self.assertEqual(retrieved_feedback.user_id, self.user.id)
        self.assertEqual(retrieved_feedback.route_id, self.route.id)
        self.assertEqual(retrieved_feedback.rating, 5)
        self.assertEqual(retrieved_feedback.comment, "Great experience!")

        # Check if relationships are correctly set
        self.assertEqual(retrieved_feedback.user, self.user)
        self.assertEqual(retrieved_feedback.route, self.route)
        self.assertIn(retrieved_feedback, self.user.feedbacks)
        self.assertIn(retrieved_feedback, self.route.feedbacks)

if __name__ == '__main__':
    unittest.main()
