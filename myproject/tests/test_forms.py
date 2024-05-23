import pytest
from django.contrib.auth.models import User
from blog.forms import PostForm, CreateUserForm, CustomAuthenticationForm

def test_PostForm_valid(db):
    form = PostForm(data={'title': 'TestTitle', 'content': 'TestContent', 'category': 1})
    assert form.is_valid()

def test_PostForm_invalid():
    form = PostForm(data={})
    assert not form.is_valid()

def test_CreateUserForm_valid(transactional_db):
    form = CreateUserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password1': 'senhafacil123', 'password2': 'senhafacil123'})
    if not form.is_valid():
        print(form.errors)
    assert form.is_valid()

def test_CreateUserForm_invalid():
    form = CreateUserForm(data={})
    assert not form.is_valid()

def test_CustomAuthenticationForm_valid(db):
    User.objects.create_user(username='testuser', password='senhafacil123')
    form = CustomAuthenticationForm(data={'username': 'testuser', 'password': 'senhafacil123'})
    assert form.is_valid()

def test_CustomAuthenticationForm_invalid(db):
    form = CustomAuthenticationForm(data={})
    assert not form.is_valid()