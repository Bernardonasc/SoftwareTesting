from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='category1')
        self.post = Post.objects.create(title='title1', content='content1', category=self.category, author=self.user)
        self.home_url = reverse('home')
        self.posts_by_category_url = reverse('posts_by_category', args=[self.category.id])
        self.register_url = reverse('register')
        self.post_detail_url = reverse('post_detail', args=[self.post.id])
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.post_create_url = reverse('post_create')
        self.post_edit_url = reverse('post_edit', args=[self.post.id])
        self.post_delete_url = reverse('post_delete', args=[self.post.id])

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_posts_by_category_GET(self):
        response = self.client.get(self.posts_by_category_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts_by_category.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_post_detail_GET(self):
        response = self.client.get(self.post_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)

    def test_post_create_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.post_create_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_form.html')

    def test_post_edit_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.post_edit_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_form.html')

    def test_post_delete_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.post_delete_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_confirm_delete.html')