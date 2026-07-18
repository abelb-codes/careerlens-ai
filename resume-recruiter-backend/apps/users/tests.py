from django.test import TestCase

from apps.users.models import User


class AuthFlowTests(TestCase):
    def test_user_model_can_be_created(self):
        user = User.objects.create_user(email="test@example.com", username="tester", password="StrongPass123")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, User.Role.CANDIDATE)
