from django.test import TestCase
from django.contrib.auth.models import User
from blog.forms import PostForm, CreateUserForm, CustomAuthenticationForm
from blog.models import Category, Post

class PostFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_PostForm_valid_data(db):
        form = PostForm(data={
            'title': 'TestTitle', 
            'content': 'TestContent', 
            'category': 1
            })
        assert form.is_valid()

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

def test_CreateUserForm_valid(transactional_db):
    form = CreateUserForm(data={'username': 'testuser', 
                                'email': 'test@example.com', 
                                'password1': 'senhafacil123', 
                                'password2': 'senhafacil123'
                                })
    if not form.is_valid():
        print(form.errors)
    assert form.is_valid()

def test_CreateUserForm_invalid():
    form = CreateUserForm(data={})
    assert not form.is_valid()

def test_CustomAuthenticationForm_valid(db):
    User.objects.create_user(username='testuser', password='senhafacil123')
    form = CustomAuthenticationForm(data={
        'username': 'testuser', 
        'password': 'senhafacil123'
        })
    assert form.is_valid()

def test_CustomAuthenticationForm_invalid(db):
    form = CustomAuthenticationForm(data={})
    assert not form.is_valid()