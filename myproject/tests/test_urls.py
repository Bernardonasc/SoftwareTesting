# tests/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import home, post_create, post_edit, post_delete, register, loginPage, logoutUser, post_detail, posts_by_category

class UrlsTest(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_post_create_url_resolves(self):
        url = reverse('post_create')
        self.assertEqual(resolve(url).func, post_create)

    def test_post_edit_url_resolves(self):
        url = reverse('post_edit', args=[1])
        self.assertEqual(resolve(url).func, post_edit)

    def test_post_delete_url_resolves(self):
        url = reverse('post_delete', args=[1])
        self.assertEqual(resolve(url).func, post_delete)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, loginPage)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logoutUser)

    def test_post_detail_url_resolves(self):
        url = reverse('post_detail', args=[1])
        self.assertEqual(resolve(url).func, post_detail)

    def test_posts_by_category_url_resolves(self):
        url = reverse('posts_by_category', args=[1])
        self.assertEqual(resolve(url).func, posts_by_category)
