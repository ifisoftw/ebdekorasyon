# Production Öncesi Yapılacaklar

## 🔴 Kritik (Zorunlu)

### 1. Content-Security-Policy (CSP)
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
CSP_IMG_SRC = ("'self'", 'data:', 'images.unsplash.com', '*.unsplash.com')
CSP_CONNECT_SRC = ("'self'",)
```

### 2. Tailwind CSS Production Build
```bash
npm install -D tailwindcss
npx tailwindcss -o static/css/tailwind.min.css --minify
```
- CDN yerine compiled CSS kullan
- `base.html`'de script'i kaldır, CSS link ekle

### 3. DEBUG = False Kontrolü
- `.env` dosyasında `DEBUG=False`
- `ALLOWED_HOSTS` doğru ayarlanmış
- Static files collectstatic yapılmış

---

## 🟡 Önerilen

### 4. Permissions-Policy Header
```python
# settings.py veya middleware
PERMISSIONS_POLICY = {
    'geolocation': [],
    'microphone': [],
    'camera': [],
}
```

### 5. Alpine.js SRI Hash
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.3/dist/cdn.min.js"
        integrity="sha384-..." crossorigin="anonymous"></script>
```

### 6. Referrer-Policy
```python
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
```

---

## 🟢 Opsiyonel

### 7. Rate Limiting (Form Spam)
```bash
pip install django-ratelimit
```

### 8. Error Pages
- `templates/404.html`
- `templates/500.html`

---

## Checklist

- [ ] CSP kuruldu ve test edildi
- [ ] Tailwind compiled CSS'e geçildi
- [ ] DEBUG=False
- [ ] collectstatic çalıştırıldı
- [ ] SSL sertifikası aktif
- [ ] Domain DNS ayarları tamam
- [ ] Permissions-Policy eklendi
- [ ] 404/500 sayfaları hazır
