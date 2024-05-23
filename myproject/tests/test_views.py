import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from blog.models import Post, Category

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