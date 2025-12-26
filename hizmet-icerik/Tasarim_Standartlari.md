# EB Dekorasyon Tasarım Standartları

## Renk Paleti

```css
/* Ana Renkler */
--eb-black: #0f0f0f;       /* Ana arka plan */
--eb-surface: #1a1a1a;     /* Kart arka planları */
--eb-surface-dark: #0a0a0a; /* Koyu yüzey */

/* Gold Tonları */
--eb-gold: #c9a465;        /* Ana altın */
--eb-gold-light: #dfc291;  /* Açık altın */
--eb-gold-dark: #b08d4a;   /* Koyu altın */

/* Metin Renkleri */
--text-white: #ffffff;
--text-gray-300: rgb(209 213 219);
--text-gray-400: rgb(156 163 175);
--text-gray-500: rgb(107 114 128);

/* WhatsApp */
--whatsapp-green: #25D366;
--whatsapp-dark: #128C7E;
```

---

## Tipografi

```css
/* Font Aileleri */
font-playfair: 'Playfair Display', serif;  /* Başlıklar */
font-inter: 'Inter', sans-serif;           /* Gövde metni */

/* Başlık Boyutları */
h1: text-4xl sm:text-5xl lg:text-6xl font-bold
h2: text-3xl sm:text-4xl lg:text-5xl font-bold  
h3: text-xl sm:text-2xl font-bold
h4: text-lg font-bold

/* Gövde Metni */
text-base: Varsayılan (16px)
text-lg: Büyük gövde (18px)
text-sm: Küçük metin (14px)
```

---

## Section Yapıları

### Hero Section
```html
<section class="relative min-h-[90vh] flex items-center overflow-hidden">
    <!-- Gradient Overlay -->
    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-[#0f0f0f]/70 to-[#0f0f0f] z-10"></div>
    
    <!-- Background Image -->
    <img class="absolute inset-0 w-full h-full object-cover" 
         fetchpriority="high" loading="eager" width="1920" height="1080">
    
    <!-- Content -->
    <div class="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
```

### Standart Section
```html
<section class="py-20 bg-[#0f0f0f]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
```

### Section Başlık Pattern
```html
<div class="text-center mb-12">
    <h2 class="font-playfair text-4xl sm:text-5xl font-bold mb-6 text-white">
        Başlık <span class="text-gold-gradient">Vurgulu Kısım</span>
    </h2>
    <p class="text-gray-400 text-lg max-w-2xl mx-auto">
        Alt açıklama metni
    </p>
</div>
```

---

## Bileşenler

### Badge/Pill
```html
<span class="inline-block px-4 py-2 rounded-full bg-[#c9a465]/20 text-[#c9a465] text-sm font-medium">
    Badge Metni
</span>
```

### Primary Button (Gold)
```html
<a class="btn-gold-gradient px-8 py-4 rounded-xl text-black font-bold text-lg flex items-center justify-center gap-3 shadow-gold-glow">
```

### Secondary Button (Outline)
```html
<button class="px-6 py-3 rounded-full font-semibold text-sm bg-transparent text-white border border-white/20 hover:border-[#c9a465] hover:text-[#c9a465] transition-all duration-300">
```

### WhatsApp Button
```html
<a class="bg-[#25D366] hover:bg-[#20bd5a] px-8 py-4 rounded-xl text-white font-bold text-lg flex items-center justify-center gap-3 transition-all">
```

### Telefon Button (CTA Strip içinde)
```html
<a class="bg-black text-white px-6 py-3 rounded-lg font-bold hover:bg-zinc-800 transition-all flex items-center gap-2">
```

---

## Kart Tasarımları

### Service / Project Card
```html
<a class="group relative h-80 rounded-2xl overflow-hidden cursor-pointer">
    <!-- Background Image -->
    <img class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
         loading="lazy" width="400" height="300">
    
    <!-- Gradient Overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent opacity-80 group-hover:opacity-90 transition-opacity"></div>
    
    <!-- Gold Border on Hover -->
    <div class="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-[#c9a465] transition-all duration-500"></div>
    
    <!-- Content -->
    <div class="absolute inset-0 p-6 flex flex-col justify-end">
        <h3 class="font-playfair text-2xl font-bold text-white mb-2 group-hover:text-[#c9a465] transition-colors duration-300">
        <p class="text-gray-300 text-sm opacity-0 group-hover:opacity-100 transform translate-y-4 group-hover:translate-y-0 transition-all duration-300">
        <!-- Arrow CTA -->
        <div class="flex items-center gap-2 text-[#c9a465] font-semibold">
            <span>İncele</span>
            <svg class="w-5 h-5 transform group-hover:translate-x-2 transition-transform duration-300">
        </div>
    </div>
</a>
```

### Feature Card
```html
<div class="bg-[#0f0f0f] rounded-xl p-6 border border-[#c9a465]/10 hover:border-[#c9a465]/30 transition-all duration-300">
    <div class="w-12 h-12 rounded-lg bg-[#c9a465]/20 flex items-center justify-center mb-4">
        <i class="text-[#c9a465] text-xl"></i>
    </div>
    <h3 class="font-playfair text-lg font-bold text-white mb-2">
    <p class="text-gray-400 text-sm">
</div>
```

---

## Özel Section'lar

### Gold CTA Strip
```html
<section class="py-6 bg-gradient-to-r from-[#b08d4a] via-[#c9a465] to-[#b08d4a]">
    <p class="text-black font-semibold text-lg">
    <a class="bg-black text-white px-6 py-3 rounded-lg font-bold">
</section>
```

### Trust Badges Strip
```html
<section class="py-8 bg-[#0a0a0a] border-y border-[#c9a465]/20">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div class="flex items-center justify-center gap-3 group">
            <div class="w-12 h-12 bg-[#1a1a1a] rounded-xl border border-[#c9a465]/30 group-hover:border-[#c9a465]">
```

---

## Animasyonlar & Geçişler

```css
/* Standart Geçiş */
transition-all duration-300

/* Kart Hover Scale */
transition-transform duration-700 group-hover:scale-110

/* Hover Translate */
transform group-hover:translate-x-2 transition-transform duration-300

/* Fade In */
opacity-0 group-hover:opacity-100 transform translate-y-4 group-hover:translate-y-0 transition-all duration-300
```

---

## Grid Sistemleri

```html
/* 3 Sütunlu Grid */
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

/* 4 Sütunlu Grid */
<div class="grid grid-cols-2 md:grid-cols-4 gap-6">

/* Flex CTA Row */
<div class="flex flex-col sm:flex-row gap-4">
```

---

## Responsive Breakpoints

```css
sm: 640px   /* flex-row, text boyutları */
md: 768px   /* grid-cols-2 */
lg: 1024px  /* grid-cols-3, büyük text */
```
