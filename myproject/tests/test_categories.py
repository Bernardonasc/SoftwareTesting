from django.test import TestCase, RequestFactory
from blog.context_processors import categories_processor
from blog.models import Category

class CategoriesProcessorTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Test Category')

    def test_categories_processor(self):
        request = self.factory.get('/')
        context = categories_processor(request)
        self.assertIn('categories', context)
        self.assertEqual(context['categories'].count(), 11) # Número inicial de categorias

    def test_multiple_categories(self):
        Category.objects.create(name='Another Category')
        request = self.factory.get('/')
        context = categories_processor(request)
        self.assertEqual(context['categories'].count(), 12)

    def test_no_categories(self):
        Category.objects.all().delete()
        request = self.factory.get('/')
        context = categories_processor(request)
        self.assertEqual(context['categories'].count(), 0)