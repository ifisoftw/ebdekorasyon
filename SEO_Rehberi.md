İFİ Yazılım - İleri Seviye Teknik SEO ve AI Entegrasyon Rehberi (2025)

Bu doküman, İFİ Yazılım'ın kurumsal projelerinde uygulanacak "Altın Standart" teknik SEO kurallarını içerir. Hedef; sadece sıralama almak değil, Google SGE (AI Overviews) ve Varlık (Entity) sonuçlarında otorite olmaktır.

1. Django Teknik Altyapı ve Tarama Bütçesi

Botların siteyi verimli ve eksiksiz taramasını sağlamak için backend yapılandırması.

1.1. Gelişmiş Sitemap Stratejisi (Görsel Destekli)

Standart URL listesi yerine, görselleri de içeren zenginleştirilmiş sitemap yapısı.

Kod Yapısı (sitemaps.py):

from django.contrib.sitemaps import Sitemap
from .models import Service

class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Service.objects.filter(is_active=True).order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    # Google Görsel İndeksleme için Kritik Metod
    def _urls(self, page, protocol, domain):
        urls = super()._urls(page, protocol, domain)
        for url in urls:
            item = self.items()[urls.index(url)]
            if item.featured_image:
                url['image'] = {
                    'loc': item.featured_image.url,
                    'title': item.title,
                    'caption': item.seo_description
                }
        return urls


✅ Bölüm Checklisti:

[ ] sitemap.xml, Sitemap Index formatında mı? (Büyük siteler için).

[ ] lastmod alanı, içerik güncellendiğinde otomatik güncelleniyor mu?

[ ] Görsel (Image) etiketleri sitemap çıktısında görünüyor mu?

1.2. Akıllı Robots.txt ve AI Kontrolü

2025'te içeriğinizin LLM modelleri tarafından eğitilmesini kontrol altına alın.

Dinamik Robots.txt View:

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /*?sort=
Disallow: /*?filter=

# Google SGE için İzin (Zorunlu)
User-agent: Googlebot
Allow: /

# İçerik Hırsızlığına Karşı AI Bot Engeli (Stratejik Karar)
User-agent: GPTBot
Disallow: /
User-agent: CCBot
Disallow: /

Sitemap: [https://www.ifiyazilim.com/sitemap.xml](https://www.ifiyazilim.com/sitemap.xml)


1.3. Canonical URL ve 410 Gone Yönetimi

Tekrarlayan içerik cezası ve silinen içeriklerin yönetimi. request.get_host yerine settings kullanımı güvenlik için şarttır.

Canonical Tag (Template):

{# settings.SITE_DOMAIN = '[www.ifiyazilim.com](https://www.ifiyazilim.com)' olmalı #}
<link rel="canonical" href="https://{{ settings.SITE_DOMAIN }}{{ request.path }}" />


Kural: Query string (?ref=...) canonical içinde asla yer almamalıdır.

410 Gone (Kalıcı Silme) View:
Silinen bir hizmetin URL'ine gelen trafiği karşılayıp botlara "Bu içerik öldü, düşür" demek için.

# views.py
from django.http import HttpResponseGone

def deleted_service_view(request, slug):
    # Eski URL pattern bu view'a yönlendirilmeli
    return HttpResponseGone("Bu hizmet artık sunulmamaktadır.")


2. İleri Seviye Schema Mimarisi (JSON-LD)

Google SGE ve LLM tabanlı arama motorlarının (ChatGPT, Perplexity) sitenizi "Otorite" olarak tanıması için zenginleştirilmiş veri yapısı.

2.1. Global Organization Schema (AI Otorite Sinyalleri)

AI botlarına "Biz kiminiz ve neyden anlarız?" sorusunun cevabını vermek için knowsAbout (Uzmanlık Alanları) özelliğini mutlaka kullanın.

templates/schemas/organization.html:

<script type="application/ld+json">
{
  "@context": "[https://schema.org](https://schema.org)",
  "@type": "Organization",
  "@id": "[https://www.ifiyazilim.com/#organization](https://www.ifiyazilim.com/#organization)",
  "name": "İFİ Yazılım",
  "url": "[https://www.ifiyazilim.com](https://www.ifiyazilim.com)",
  "logo": "[https://www.ifiyazilim.com/static/img/logo.png](https://www.ifiyazilim.com/static/img/logo.png)",
  "sameAs": [
    "[https://www.linkedin.com/company/ifiyazilim](https://www.linkedin.com/company/ifiyazilim)",
    "[https://instagram.com/ifiyazilim](https://instagram.com/ifiyazilim)",
    "[https://twitter.com/ifiyazilim](https://twitter.com/ifiyazilim)"
  ],
  "knowsAbout": [
    "Kurumsal Web Tasarım",
    "Django Geliştirme",
    "E-Ticaret Altyapısı",
    "SEO Optimizasyonu"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+90-850-123-4567",
    "contactType": "customer service",
    "areaServed": "TR",
    "availableLanguage": ["Turkish", "English"]
  }
}
</script>


2.2. Service ve Offer Şeması (Ticari Odak)

templates/schemas/service.html:

<script type="application/ld+json">
{
  "@context": "[https://schema.org](https://schema.org)",
  "@type": "Service",
  "name": "{{ service.title }}",
  "provider": { "@id": "[https://www.ifiyazilim.com/#organization](https://www.ifiyazilim.com/#organization)" },
  "areaServed": {
    "@type": "AdministrativeArea",
    "name": "{{ service.area.name|default:'Türkiye' }}"
  },
  "description": "{{ service.seo_description }}",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Hizmet Paketleri",
    "itemListElement": [
      {% for sub in service.sub_services.all %}
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "{{ sub.name }}"
        }
      }{% if not forloop.last %},{% endif %}
      {% endfor %}
    ]
  }
}
</script>


2.3. AI ve Sesli Arama İçin FAQPage Şeması (Kritik)

AI özetleri (AI Overviews), genellikle "Sıkça Sorulan Sorular" yapısındaki net cevapları kaynak olarak kullanır. Her hizmet sayfasının altına eklenen SSS modülü JSON-LD olarak işaretlenmelidir.

templates/schemas/faq.html:

{% if faq_list %}
<script type="application/ld+json">
{
  "@context": "[https://schema.org](https://schema.org)",
  "@type": "FAQPage",
  "mainEntity": [
    {% for faq in faq_list %}
    {
      "@type": "Question",
      "name": "{{ faq.question }}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{ faq.answer|striptags }}"
      }
    }{% if not forloop.last %},{% endif %}
    {% endfor %}
  ]
}
</script>
{% endif %}


✅ Bölüm Checklisti:

[ ] Google Rich Results Test ile tüm şemalar doğrulandı mı?

[ ] Organization şemasında knowsAbout alanları sektör anahtar kelimeleriyle dolduruldu mu?

[ ] Hizmet detay sayfalarında FAQ şeması dinamik olarak basılıyor mu?

 

Spam (Doorway Page) cezası almadan binlerce lokasyon sayfası oluşturmanın yolu.

3.1. Riskli "Spintax" Yerine "Veri Enjeksiyonu"

Google, sadece kelime değiştiren sayfaları cezalandırır. Sayfayı o lokasyona özel verilerle zenginleştirmelisiniz.

Yanlış (Riskli): "{İstanbul|Ankara} web tasarım." (Sadece kelime değişiyor)

Doğru (Data-Driven):

Veritabanında her ilçe için gerçek veriler tutun: population, distance_to_center, local_referance.

Template:

"{{ district.name }} ilçesindeki {{ district.population }} işletme için dijital çözümler sunuyoruz. Merkez şubemize {{ district.distance }} km uzaklıktaki işletmenize yerinde destek veriyoruz."

3.2. URL Yapısı

/hizmet/<slug:service_slug>/<slug:location_slug>/

✅ Bölüm Checklisti:

[ ] Oluşturulan sayfalar sadece kelime değişikliği mi içeriyor, yoksa o bölgeye özel benzersiz veri var mı?

[ ] Sayfalar arası "Internal Linking" (İç Linkleme) kurgusu var mı?

4. İçerik Optimizasyonu ve SGE (AI Overviews)

4.1. "Direct Answer" Blokları

Her makalenin girişinde, sorunun cevabını net veren 40-60 kelimelik bir özet bulunmalıdır.

HTML: <div class="direct-answer bg-gray-50 p-4 font-medium">...</div>

4.2. Yapılandırılmış Veri

Fiyat tabloları ve özellik listeleri mutlaka HTML <table>, <ul> etiketleri ile sunulmalıdır. AI modelleri CSS grid tablolarını anlamakta zorlanabilir.

5. Otomatik SEO Testleri (QA Pipeline)

Yazılım ekibinin SEO'yu bozmasını engellemek için CI/CD sürecine eklenecek testler.

tests/test_seo.py:

from django.test import TestCase
from django.urls import reverse
from django.conf import settings

class SEOTestCase(TestCase):
    def test_homepage_seo(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Meta Description Var mı?
        self.assertContains(response, '<meta name="description"')
        # Canonical Var mı?
        self.assertContains(response, f'<link rel="canonical" href="https://{settings.SITE_DOMAIN}')
        # H1 Etiketi Var mı?
        self.assertContains(response, '<h1')


6. Ekstra: X-Robots-Tag ve Server Timing

Mükemmeliyet için sunucu seviyesi ayarlar.

PDF ve Dosyalar için Noindex:
Google'ın PDF dosyalarını tarayıp duplicate content oluşturmasını engellemek için Nginx ayarı:

location ~* \.(pdf|doc|docx)$ {
    add_header X-Robots-Tag "noindex, nofollow";
}


Debug İçin Server-Timing:
Backend işlemlerinin ne kadar sürdüğünü tarayıcı console'unda görmek için (INP optimizasyonu):

# Middleware veya View içinde
response['Server-Timing'] = f'db;dur={db_time}, render;dur={render_time}'


Bu döküman, projenin "Canlıya Alım (Go-Live)" aşamasından önce Teknik Ekip Lideri tarafından onaylanmalıdır.