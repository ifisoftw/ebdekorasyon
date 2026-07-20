from django.test import TestCase, Client
from django.urls import reverse
from service.models import (
    ServiceCategory, Service, ServiceArea, ServiceStep, ServiceHeader
)
from core.models import Settings


class ServiceCategoryModelTests(TestCase):
    """ServiceCategory model testleri"""
    
    def test_category_creation(self):
        """Kategori oluşturma testi"""
        category = ServiceCategory.objects.create(
            name='İç Mekan',
            slug='ic-mekan',
            icon='fas fa-home',
            order=1
        )
        self.assertEqual(str(category), 'İç Mekan')
        self.assertTrue(category.is_active)
        self.assertEqual(category.order, 1)
    
    def test_category_ordering(self):
        """Kategori sıralama testi"""
        cat1 = ServiceCategory.objects.create(name='Z Kategori', slug='z-kategori', order=2)
        cat2 = ServiceCategory.objects.create(name='A Kategori', slug='a-kategori', order=1)
        categories = list(ServiceCategory.objects.all())
        self.assertEqual(categories[0], cat2)  # order=1 önce gelmeli


class ServiceModelTests(TestCase):
    """Service model testleri"""
    
    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Dekorasyon',
            slug='dekorasyon'
        )
        self.service = Service.objects.create(
            title='Duvar Kağıdı',
            slug='duvar-kagidi',
            description='Profesyonel duvar kağıdı uygulaması',
            short_description='Duvar kağıdı hizmeti',
            category=self.category
        )
    
    def test_service_creation(self):
        """Hizmet oluşturma testi"""
        self.assertEqual(str(self.service), 'Duvar Kağıdı')
        self.assertTrue(self.service.isActive)
        self.assertTrue(self.service.showIndex)
    
    def test_service_absolute_url(self):
        """Hizmet absolute URL testi"""
        expected_url = reverse('service_detail', args=['duvar-kagidi'])
        self.assertEqual(self.service.get_absolute_url(), expected_url)
    
    def test_service_category_relation(self):
        """Hizmet-Kategori ilişki testi"""
        self.assertEqual(self.service.category, self.category)
        self.assertIn(self.service, self.category.services.all())


class ServiceStepModelTests(TestCase):
    """ServiceStep model testleri"""
    
    def setUp(self):
        self.service = Service.objects.create(
            title='Boya Hizmeti',
            slug='boya-hizmeti',
            description='Boya açıklaması',
            short_description='Boya kısa açıklama'
        )
        self.step1 = ServiceStep.objects.create(
            service=self.service,
            step_number=1,
            title='Keşif',
            description='Yerinde keşif yapılır'
        )
        self.step2 = ServiceStep.objects.create(
            service=self.service,
            step_number=2,
            title='Uygulama',
            description='Boya uygulaması yapılır'
        )
    
    def test_step_creation(self):
        """Adım oluşturma testi"""
        self.assertEqual(str(self.step1), 'Boya Hizmeti - Adım 1')
    
    def test_step_ordering(self):
        """Adım sıralama testi"""
        steps = list(self.service.steps.all())
        self.assertEqual(steps[0].step_number, 1)
        self.assertEqual(steps[1].step_number, 2)


class ServiceAreaModelTests(TestCase):
    """ServiceArea model testleri"""
    
    def test_service_area_creation(self):
        """Hizmet bölgesi oluşturma testi"""
        area = ServiceArea.objects.create(
            title='Kadıköy',
            slug='kadikoy',
            description='Kadıköy bölgesi hizmetleri',
            short_description='Kadıköy hizmet bölgesi',
            icon='fas fa-map-marker'
        )
        self.assertEqual(str(area), 'Kadıköy')
        self.assertTrue(area.isActive)


class ServiceHeaderModelTests(TestCase):
    """ServiceHeader model testleri"""
    
    def test_header_creation(self):
        """Header oluşturma testi"""
        header = ServiceHeader.objects.create(
            title='Hizmetlerimiz',
            description='Tüm hizmetlerimiz burada'
        )
        self.assertEqual(str(header), 'Hizmetlerimiz')


class ServiceViewTests(TestCase):
    """Service view testleri"""
    
    def setUp(self):
        self.client = Client()
        # Template'ler Settings'e ihtiyaç duyuyor
        self.settings = Settings.objects.create(
            name='Test Site',
            seo_title='Test SEO',
            seo_description='Test Description'
        )
        self.category = ServiceCategory.objects.create(
            name='Test Kategori',
            slug='test-kategori'
        )
        self.service = Service.objects.create(
            title='Test Hizmet',
            slug='test-hizmet',
            description='Test açıklama',
            short_description='Test kısa açıklama',
            category=self.category,
            isActive=True
        )
        self.inactive_service = Service.objects.create(
            title='Pasif Hizmet',
            slug='pasif-hizmet',
            description='Pasif açıklama',
            short_description='Pasif kısa açıklama',
            isActive=False
        )
    
    def test_service_list_200(self):
        """Hizmet listesi sayfası 200 döndürmeli"""
        url = reverse('services')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_service_detail_200(self):
        """Hizmet detay sayfası 200 döndürmeli"""
        url = reverse('service_detail', args=[self.service.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_service_detail_404(self):
        """Olmayan hizmet 404 döndürmeli"""
        url = reverse('service_detail', args=['olmayan-hizmet'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ServiceAreaViewTests(TestCase):
    """ServiceArea view testleri"""
    
    def setUp(self):
        self.client = Client()
        # Template'ler Settings'e ihtiyaç duyuyor
        self.settings = Settings.objects.create(
            name='Test Site',
            seo_title='Test SEO',
            seo_description='Test Description'
        )
        self.area = ServiceArea.objects.create(
            title='Test Bölge',
            slug='test-bolge',
            description='Test bölge açıklaması',
            short_description='Test bölge kısa açıklama',
            isActive=True
        )
    
    def test_service_area_list_200(self):
        """Hizmet bölgesi listesi 200 döndürmeli"""
        url = reverse('service_areas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_service_area_detail_200(self):
        """Hizmet bölgesi detay sayfası 200 döndürmeli"""
        # ServiceArea detayları service_detail URL'ini kullanıyor
        url = reverse('service_detail', args=[self.area.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ServiceURLTests(TestCase):
    """Service URL testleri"""
    
    def test_service_urls_exist(self):
        """Service URL'leri mevcut olmalı"""
        self.assertTrue(reverse('services'))
        self.assertTrue(reverse('service_areas'))
