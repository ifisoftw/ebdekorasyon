# PageSpeed 100 Kuralları

Bu doküman, tüm sayfa şablonlarında uygulanması gereken Lighthouse 100 puan kurallarını içerir.

---

## 1. Performance

### Hero Görsel (LCP)
```html
<img src="..." 
     alt="Açıklayıcı metin" 
     fetchpriority="high"
     loading="eager"
     width="1920" height="1080">
```

### Diğer Görseller
```html
<img src="..." 
     alt="Açıklayıcı metin" 
     loading="lazy"
     width="400" height="300">
```

### Preconnect (base.html)
```html
<link rel="preconnect" href="https://cdn.tailwindcss.com">
<link rel="preconnect" href="https://cdnjs.cloudflare.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
```

---

## 2. Accessibility

### Skip Link (base.html)
```html
<a href="#main-content" class="sr-only focus:not-sr-only ...">
    Ana içeriğe geç
</a>
```

### Main Landmark
```html
<main id="main-content" role="main">
```

### Buton Aria Labels
```html
<button aria-label="Menüyü aç/kapat" :aria-expanded="open">
```

### Alt Text
- Tüm görsellerde açıklayıcı alt text
- Dekoratif görseller: `alt=""`

---

## 3. Best Practices

### External Links
```html
<a href="..." target="_blank" rel="noopener">
```

### Theme Color
```html
<meta name="theme-color" content="#0f0f0f">
```

---

## 4. SEO

### Required Meta Tags
```html
<title>Sayfa Başlığı | Site Adı</title>
<meta name="description" content="150-160 karakter">
<link rel="canonical" href="https://domain.com/sayfa/">
```

### Schema Markup
- Organization: `schemas/organization.html` (base.html'de)
- FAQPage: `schemas/faq.html` (SSS olan sayfalarda)
- Article: Blog detay sayfalarında
- Service: Hizmet detay sayfalarında

### Tek H1 Kuralı
Her sayfada yalnızca 1 adet `<h1>` etiketi olmalı.

---

## Checklist

Her yeni sayfa için:
- [ ] `{% block title %}` tanımlı
- [ ] `{% block meta_description %}` tanımlı  
- [ ] Tek H1 etiketi var
- [ ] Hero görsel: `fetchpriority="high"`, `loading="eager"`
- [ ] Diğer görseller: `loading="lazy"`, `width`, `height`
- [ ] Butonlarda `aria-label`
- [ ] External linklerde `rel="noopener"`
- [ ] Gerekli schema include edilmiş
