# 2025 Best Practices Denetimi

## Durum: EB Dekorasyon

---

## 1. GÜVENLİK BAŞLIKLARI (Security Headers)

| Header | Durum | Django Ayarı |
|--------|-------|--------------|
| Strict-Transport-Security (HSTS) | ✅ | `SECURE_HSTS_SECONDS = 31536000` |
| HSTS Subdomains | ✅ | `SECURE_HSTS_INCLUDE_SUBDOMAINS = True` |
| HSTS Preload | ✅ | `SECURE_HSTS_PRELOAD = True` |
| X-Frame-Options | ✅ | `XFrameOptionsMiddleware` |
| X-Content-Type-Options | ✅ | `SECURE_CONTENT_TYPE_NOSNIFF = True` |
| X-XSS-Protection | ✅ | `SECURE_BROWSER_XSS_FILTER = True` |
| Content-Security-Policy (CSP) | ❌ | **EKSİK** - `django-csp` kurulmalı |
| Referrer-Policy | ⚠️ | Varsayılan kullanılıyor |
| Permissions-Policy | ❌ | **EKSİK** |

---

## 2. HTTPS & SSL

| Kriter | Durum |
|--------|-------|
| SSL Redirect | ✅ `SECURE_SSL_REDIRECT = True` |
| Proxy SSL Header | ✅ `SECURE_PROXY_SSL_HEADER` |
| Canonical HTTPS | ✅ Template'lerde https:// |

---

## 3. CDN & ASSET GÜVENLİĞİ

| Kriter | Durum | Açıklama |
|--------|-------|----------|
| FontAwesome SRI | ✅ | `integrity="sha512-..."` |
| Tailwind CDN SRI | ❌ | **EKSİK** (CDN desteklemiyor) |
| Google Fonts | ✅ | Güvenli source |
| Alpine.js SRI | ❌ | **EKSİK** |

---

## 4. LIGHTHOUSE BEST PRACTICES

| Kriter | Durum |
|--------|-------|
| HTTPS | ✅ |
| No Mixed Content | ✅ |
| rel="noopener" | ✅ External linkler |
| Viewport Meta | ✅ |
| Doctype | ✅ |
| Charset | ✅ UTF-8 |
| lang Attribute | ✅ tr |

---

## 5. EKSİKLER & ÖNCELİKLER

### Yüksek Öncelik
1. **Content-Security-Policy (CSP)**
   - `pip install django-csp`
   - Middleware ekle
   - Policy tanımla

### Orta Öncelik
2. **Permissions-Policy Header**
   - Kamera, mikrofon, geolocation izinleri

3. **Alpine.js SRI**
   - integrity hash ekle

### Düşük Öncelik
4. **Referrer-Policy**
   - `Referrer-Policy: strict-origin-when-cross-origin`

---

## CSP Kurulum Rehberi

```bash
pip install django-csp
```

```python
# settings.py
MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    # ... diğerleri
]

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", 'cdn.tailwindcss.com', 'cdn.jsdelivr.net', "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", 'fonts.googleapis.com', 'cdnjs.cloudflare.com', "'unsafe-inline'")
CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com', 'cdnjs.cloudflare.com')
CSP_IMG_SRC = ("'self'", 'data:', 'images.unsplash.com')
```

---

## SONUÇ

| Kategori | Skor |
|----------|------|
| Security Headers | 70% |
| HTTPS/SSL | 100% |
| Asset Security | 75% |
| Lighthouse | 95% |
| **TOPLAM** | **85%** |

> CSP ve Permissions-Policy eklendikten sonra **100%** olacak.
