from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Post

class CategoryModelTest(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            category=self.category,
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test Content')
        self.assertEqual(self.post.category.name, 'Test Category')
        self.assertEqual(self.post.author.username, 'testuser')

    def test_post_default_values(self):
        post = Post.objects.create(title='Another Test Post', author=self.user)
        self.assertIsNone(post.category)
        self.assertEqual(post.content, '')

    def test_post_update(self):
        self.post.title = 'Updated Test Post'
        self.post.save()
        self.assertEqual(self.post.title, 'Updated Test Post')

    def test_post_delete(self):
        post_id = self.post.id
        self.post.delete()
        self.assertFalse(Post.objects.filter(id=post_id).exists())

    def test_post_author(self):
        self.assertEqual(self.post.author, self.user)

    def test_post_category(self):
        self.assertEqual(self.post.category, self.category)

    def test_multiple_posts_same_category(self):
        post2 = Post.objects.create(
            title='Second Test Post',
            content='Second Test Content',
            category=self.category,
            author=self.user
        )
        self.assertEqual(post2.category, self.category)

    def test_post_creation_without_category(self):
        post = Post.objects.create(
            title='No Category Post',
            content='No Category Content',
            author=self.user
        )
        self.assertIsNone(post.category)

    def test_post_creation_with_different_author(self):
        user2 = User.objects.create_user(username='testuser2', password='12345')
        post = Post.objects.create(
            title='Different Author Post',
            content='Different Author Content',
            category=self.category,
            author=user2
        )
        self.assertEqual(post.author, user2)

    def test_post_content_field(self):
        self.assertEqual(self.post.content, 'Test Content')

    def test_category_field(self):
        self.assertEqual(self.post.category.name, 'Test Category')

    def test_created_at_field(self):
        self.assertIsNotNone(self.post.created_at)

    def test_updated_at_field(self):
        self.assertIsNotNone(self.post.updated_at)

    def test_post_content_max_length(self):
        long_content = 'a' * 5000
        post = Post.objects.create(
            title='Long Content Post',
            content=long_content,
            category=self.category,
            author=self.user
        )
        self.assertEqual(post.content, long_content)
