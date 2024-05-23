import pytest
from django.contrib.auth.models import User

@pytest.fixture
def user1(db):
    return User.objects.create_user(username='testuser1', password='12345')

def test_user_creation(user1):
    assert user1.username == 'testuser1'

def test_default_user_is_active(user1):
    assert user1.is_active == True

def test_default_user_is_not_staff(user1):
    assert user1.is_staff == False

def test_default_user_is_not_superuser(user1):
    assert user1.is_superuser == False