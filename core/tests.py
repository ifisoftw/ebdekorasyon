from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Settings, Contact, About
from .forms import ContactForm
import tempfile
import os
from django.conf import settings


class CoreViewsTestCase(TestCase):
    
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def setUp(self):
        self.client = Client()
        # Test için gerekli Settings objesi oluştur
        self.settings = Settings.objects.create(
            name='Test Nakliyat',
            seo_title='Test SEO Title',
            seo_description='Test SEO Description'
        )
        # Test için About objesi oluştur
        self.about = About.objects.create(
            header='Test Header',
            title='Test Title',
            description='Test Description',
            short_description='Test Short Description',
            mission='Test Mission',
            vision='Test Vision'
        )
        
    def test_contact_form_valid_submission(self):
        """Test valid contact form submission"""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '05551234567',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        
        # Check if contact was created
        self.assertTrue(Contact.objects.filter(name='Test User').exists())


class CoreViewsSimpleTestCase(TestCase):
    """Simplified tests that don't require template rendering"""
    
    def test_views_exist(self):
        """Test that URL patterns are configured correctly"""
        # Test URL reverse works
        self.assertTrue(reverse('index'))
        self.assertTrue(reverse('about'))
        self.assertTrue(reverse('contact'))
        
    def test_contact_form_valid_submission_no_template(self):
        """Test valid contact form submission without template rendering"""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '05551234567',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        
        # Check if contact was created
        self.assertTrue(Contact.objects.filter(name='Test User').exists())


class ContactFormTestCase(TestCase):
    def test_contact_form_valid(self):
        """Test contact form with valid data"""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '05551234567',
            'subject': 'Test Subject',
            'message': 'This is a test message with more than 10 characters.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_contact_form_invalid_phone(self):
        """Test contact form with invalid phone"""
        form_data = {
            'name': 'Test User',
            'phone': '123',  # Invalid phone
            'message': 'This is a test message with more than 10 characters.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_contact_form_short_message(self):
        """Test contact form with short message"""
        form_data = {
            'name': 'Test User',
            'phone': '05551234567',
            'message': 'Short'  # Too short
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())


class ModelsTestCase(TestCase):
    def test_settings_model(self):
        """Test Settings model"""
        settings = Settings.objects.create(
            name='Test Company',
            email='test@example.com',
            seo_title='Test SEO Title'
        )
        self.assertEqual(str(settings), 'Test Company')
        
    def test_contact_model(self):
        """Test Contact model"""
        contact = Contact.objects.create(
            name='Test User',
            email='test@example.com',
            phone='05551234567',
            message='Test message'
        )
        self.assertEqual(str(contact), 'Test User')
        self.assertFalse(contact.isRead)  # Default should be False


class RobotsSitemap404Tests(TestCase):
    def setUp(self):
        self.settings = Settings.objects.create(name="Test Site")

    def test_robots_txt_200_if_enabled(self):
        # By default enable_robots_txt is True
        resp = self.client.get(reverse('robots_txt'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Sitemap:")

    def test_robots_txt_disallow_if_disabled(self):
        self.settings.enable_robots_txt = False
        self.settings.save()
        resp = self.client.get(reverse('robots_txt'))
        self.assertEqual(resp.status_code, 200)
        # Should contain "Disallow: /"
        self.assertContains(resp, "Disallow: /")

    def test_sitemap_xml_200(self):
        resp = self.client.get('/sitemap.xml')
        self.assertEqual(resp.status_code, 200)

    def test_unknown_url_404(self):
        resp = self.client.get('/bu-url-yok-404/')
        self.assertEqual(resp.status_code, 404)

class StaticPageSmokeTests(TestCase):
    def setUp(self):
        Settings.objects.create(name="Statik Site")

    def test_pages_200(self):
        # List of static page URL names to test
        pages = ['privacy_policy', 'terms_of_service', 'kvkk']
        for page_name in pages:
            url = reverse(page_name)
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, f"{page_name} failed")
