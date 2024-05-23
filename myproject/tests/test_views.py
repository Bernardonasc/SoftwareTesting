import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from blog.models import Post, Category
from blog.views import CreateUserForm

@pytest.fixture
def client(db):
    return Client()

@pytest.fixture
def user(transactional_db):
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def category(transactional_db):
    return Category.objects.create(name='TestCategory')

@pytest.fixture
def post(transactional_db, user, category):
    return Post.objects.create(title='TestPost', content='TestContent', author=user, category=category)

def test_home_GET(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200

def test_posts_by_category_GET(client, category):
    response = client.get(reverse('posts_by_category', args=[category.id]))
    assert response.status_code == 200

def test_register_GET(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200

def test_post_detail_GET(client, post):
    response = client.get(reverse('post_detail', args=[post.id]))
    assert response.status_code == 200

def test_loginPage_GET(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200

def test_post_create_GET(client, user):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('post_create'))
    assert response.status_code == 200

def test_post_edit_GET(client, user, post):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('post_edit', args=[post.id]))
    assert response.status_code == 200

def test_post_delete_GET(client, user, post):
    client.login(username='testuser', password='12345')
    response = client.get(reverse('post_delete', args=[post.id]))
    assert response.status_code == 200

def test_logout_GET_is_redirected(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302

def test_login_POST_is_redirected(client, user):
    response = client.post(reverse('login'), {'username':
                                                'testuser', 'password': '12345'})
    assert response.status_code == 302

def test_login_POST_goes_to_home(client, user):
    response = client.post(reverse('login'), {'username':
                                                'testuser', 'password': '12345'})
    assert response.url == reverse('home')

def test_CreateUserForm_password_mismatch(transactional_db):
    form = CreateUserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password1': 'password123', 'password2': 'password321'})
    assert not form.is_valid()
    assert form.errors['password2'] == ["The two password fields didn’t match."]

def test_CreateUserForm_short_password(transactional_db):
    form = CreateUserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password1': 'pwd', 'password2': 'pwd'})
    assert not form.is_valid()
    assert form.errors['password2'] == ['This password is too short. It must contain at least 8 characters.']

def test_CreateUserForm_common_password(transactional_db):
    form = CreateUserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password1': 'password', 'password2': 'password'})
    assert not form.is_valid()
    assert form.errors['password2'] == ['This password is too common.']