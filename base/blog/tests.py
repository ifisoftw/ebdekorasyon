from django.test import TestCase
from django.urls import reverse
from blog.models import Blog, Category


class BlogSmokeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Genel", slug="genel")
        self.blog = Blog.objects.create(
            title="Test Blog",
            slug="test-blog",
            description="Açıklama",
            short_description="Kısa açıklama",
            category=self.category,
        )

    def test_blog_list_200(self):
        url = reverse("blogs")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_blog_detail_200(self):
        url = reverse("blog_detail", args=[self.blog.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_blog_detail_404(self):
        url = reverse("blog_detail", args=["yok-blog"])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

# Create your tests here.
