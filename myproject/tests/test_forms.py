from django.test import TestCase
from django.contrib.auth.models import User
from blog.forms import PostForm, CreateUserForm
from blog.models import Category, Post

class PostFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_post_form_valid_data(self):
        form = PostForm(data={
            'title': 'Test Post',
            'content': 'Test Content',
            'category': self.category.id
        })
        self.assertTrue(form.is_valid())

    def test_post_form_no_title(self):
        form = PostForm(data={
            'title': '',
            'content': 'Test Content',
            'category': self.category.id
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('title', form.errors)

    def test_post_form_no_content(self):
        form = PostForm(data={
            'title': 'Test Post',
            'content': '',
            'category': self.category.id
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('content', form.errors)

    def test_post_form_invalid_category(self):
        form = PostForm(data={
            'title': 'Test Post',
            'content': 'Test Content',
            'category': 999
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('category', form.errors)

    def test_post_form_missing_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)
        self.assertIn('category', form.errors)

class CreateUserFormTest(TestCase):

    def test_create_user_form_valid_data(self):
        form = CreateUserForm(data={
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_create_user_form_password_mismatch(self):
        form = CreateUserForm(data={
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'differentpassword456'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('password2', form.errors)

    def test_create_user_form_no_username(self):
        form = CreateUserForm(data={
            'username': '',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)

    def test_create_user_form_no_password(self):
        form = CreateUserForm(data={
            'username': 'newuser',
            'password1': '',
            'password2': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_create_user_form_missing_data(self):
        form = CreateUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        self.assertIn('username', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)
