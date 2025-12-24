from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Blog, Category, Tag


class CategoryModelTests(TestCase):
    """Category model testleri"""
    
    def test_category_creation(self):
        """Kategori oluşturma testi"""
        category = Category.objects.create(name='Dekorasyon', slug='dekorasyon')
        self.assertEqual(str(category), 'Dekorasyon')
    
    def test_category_unique_slug(self):
        """Kategori slug benzersiz olmalı"""
        Category.objects.create(name='Test', slug='test')
        with self.assertRaises(Exception):
            Category.objects.create(name='Test 2', slug='test')


class TagModelTests(TestCase):
    """Tag model testleri"""
    
    def test_tag_creation(self):
        """Etiket oluşturma testi"""
        tag = Tag.objects.create(name='DIY', slug='diy')
        self.assertEqual(str(tag), 'DIY')


class BlogModelTests(TestCase):
    """Blog model testleri"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Genel', slug='genel')
        self.tag = Tag.objects.create(name='Trend', slug='trend')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            description='Açıklama',
            short_description='Kısa açıklama',
            category=self.category,
        )
        self.blog.tags.add(self.tag)
    
    def test_blog_creation(self):
        """Blog oluşturma testi"""
        self.assertEqual(str(self.blog), 'Test Blog')
        self.assertTrue(self.blog.isActive)
        self.assertTrue(self.blog.showIndex)
    
    def test_blog_absolute_url(self):
        """Blog absolute URL testi"""
        expected_url = reverse('blog_detail', args=['test-blog'])
        self.assertEqual(self.blog.get_absolute_url(), expected_url)
    
    def test_blog_tags_relation(self):
        """Blog-Tag ilişki testi"""
        self.assertIn(self.tag, self.blog.tags.all())


class BlogViewTests(TestCase):
    """Blog view testleri"""
    
    def setUp(self):
        self.client = Client()
        # Template'ler Settings'e ihtiyaç duyuyor
        from core.models import Settings
        self.settings = Settings.objects.create(
            name='Test Site',
            seo_title='Test SEO',
            seo_description='Test Description'
        )
        self.category = Category.objects.create(name='Genel', slug='genel')
        self.blog = Blog.objects.create(
            title='Test Blog',
            slug='test-blog',
            description='Açıklama',
            short_description='Kısa açıklama',
            category=self.category,
        )

    def test_blog_list_200(self):
        """Blog listesi sayfası 200 döndürmeli"""
        url = reverse('blogs')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_blog_detail_200(self):
        """Blog detay sayfası 200 döndürmeli"""
        url = reverse('blog_detail', args=[self.blog.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_blog_detail_404(self):
        """Olmayan blog 404 döndürmeli"""
        url = reverse('blog_detail', args=['yok-blog'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
