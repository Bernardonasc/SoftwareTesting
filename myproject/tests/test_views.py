from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category

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
