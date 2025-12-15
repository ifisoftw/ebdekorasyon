from django.test import TestCase
from django.urls import reverse
from service.models import Service, ServiceArea


class ServiceSmokeTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            title="Test Servis",
            slug="test-servis",
            description="Açıklama",
            short_description="Kısa açıklama",
        )
        self.service_area = ServiceArea.objects.create(
            title="Test Hizmet Bölgesi",
            slug="test-bolge",
            description="Bölge Açıklama",
            short_description="Bölge Kısa açıklama",
        )

    def test_service_list_200(self):
        url = reverse("services")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_service_detail_200(self):
        url = reverse("service_detail", args=[self.service.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_service_detail_404(self):
        url = reverse("service_detail", args=["yok-servis"])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_service_area_list_200(self):
        url = reverse("service_areas")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_service_area_detail_200(self):
        # ServiceArea uses the same URL pattern but different lookup
        url = reverse("service_detail", args=[self.service_area.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Test Hizmet Bölgesi")

    def test_slug_collision_precedence(self):
        # Create a ServiceArea with same slug as Service
        # Service should take precedence
        ServiceArea.objects.create(
            title="Collision Area",
            slug="test-servis", # Same as self.service.slug
            description="Collision",
            short_description="Collision"
        )
        
        url = reverse("service_detail", args=["test-servis"])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Should show Service content, not ServiceArea
        self.assertContains(resp, "Test Servis")
        self.assertNotContains(resp, "Collision Area")

# Create your tests here.
