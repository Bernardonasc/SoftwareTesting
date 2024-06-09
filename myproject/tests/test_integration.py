from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category

class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_post(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'Integration Test Post',
            'content': 'This is a test post',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Post.objects.filter(title='Integration Test Post').exists())

    def test_view_post(self):
        post = Post.objects.create(
            title='View Test Post',
            content='Test Content',
            category=self.category,
            author=self.user
        )
        response = self.client.get(reverse('post_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Test Post')

    def test_edit_post(self):
        post = Post.objects.create(
            title='Edit Test Post',
            content='Test Content',
            category=self.category,
            author=self.user
        )
        response = self.client.post(reverse('post_edit', args=[post.pk]), {
            'title': 'Edited Test Post',
            'content': 'Edited Content',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Edited Test Post')

    def test_delete_post(self):
        post = Post.objects.create(
            title='Delete Test Post',
            content='Test Content',
            category=self.category,
            author=self.user
        )
        response = self.client.post(reverse('post_delete', args=[post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_register_user(self):
        self.client.logout()
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(User.objects.filter(username='newuser').exists())

        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

        login_response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'complexpassword123'
        })
        self.assertEqual(login_response.status_code, 302) 
        self.assertTrue(User.objects.filter(username='newuser').exists())
