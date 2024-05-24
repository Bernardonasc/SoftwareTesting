import pytest
from django.test import TestCase, Client
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
    return Post.objects.create(
        title='TestPost',
        content='TestContent',
        author=user, 
        category=category)

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
    form = CreateUserForm(data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'password123',
        'password2': 'password321'
    })
    assert not form.is_valid()
    assert form.errors['password2'] == ["The two password fields didn’t match."]

def test_CreateUserForm_short_password(transactional_db):
    form = CreateUserForm(data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'pwd',
        'password2': 'pwd'
    })
    assert not form.is_valid()
    assert form.errors['password2'] == ['This password is too short. It must contain at least 8 characters.']

def test_CreateUserForm_common_password(transactional_db):
    form = CreateUserForm(data={
        'username': 'testuser', 
        'email': 'test@example.com', 
        'password1': 'password', 
        'password2': 'password'
        })
    assert not form.is_valid()
    assert form.errors['password2'] == ['This password is too common.']

class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            category=self.category,
            author=self.user
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Test Post')

    def test_home_view_pagination(self):
        for i in range(7):
            Post.objects.create(
                title=f'Test Post {i+2}',
                content='Test Content',
                category=self.category,
                author=self.user
            )
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Page 1 of 2')

    def test_home_view_query(self):
        response = self.client.get(reverse('home') + '?q=Test')
        self.assertContains(response, 'Test Post')

    def test_home_view_invalid_query(self):
        response = self.client.get(reverse('home') + '?q=Invalid')
        self.assertNotContains(response, 'Test Post')

class PostDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            category=self.category,
            author=self.user
        )

    def test_post_detail_view_status_code(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_template(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_detail_view_content(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertContains(response, 'Test Post')

    def test_post_detail_view_invalid_post(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

class PostCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_post_create_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_form.html')

    def test_post_create_view_post_invalid(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_create'), {
            'title': '',
            'content': 'New Content'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_form.html')

    def test_post_create_view_not_logged_in(self):
        response = self.client.get(reverse('post_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('post_create')}")