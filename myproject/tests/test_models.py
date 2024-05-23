from django.test import TestCase
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')

    def test_user_creation(self):
        self.assertEquals(self.user1.username, 'testuser1')

    def test_default_user_is_active(self):
        self.assertEquals(self.user1.is_active, True)

    def test_default_user_is_not_staff(self):
        self.assertEquals(self.user1.is_staff, False)

    def test_default_user_is_not_superuser(self):
        self.assertEquals(self.user1.is_superuser, False)