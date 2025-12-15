from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from . models import Contact
from service.models import Service
import re
class ContactForm(forms.ModelForm):
    # Telefon numarası validator
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Telefon numarası geçerli formatta olmalıdır. Örnek: +905551234567"
    )
    
    name = forms.CharField(
        label="",
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'İsim Soyisim',
            'required': 'required',
        }),
        error_messages={
            'required': 'İsim soyisim alanı zorunludur.',
            'min_length': 'İsim soyisim en az 2 karakter olmalıdır.',
            'max_length': 'İsim soyisim en fazla 100 karakter olabilir.'
        }
    )

    email = forms.EmailField(
        label='',
        required=False,  # Opsiyonel olarak işaretlenmiş
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E Posta (Opsiyonel)',
        }),
        error_messages={
            'invalid': 'Geçerli bir e-posta adresi giriniz.'
        }
    )
  
    phone = forms.CharField(
        label='',
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Telefon',
            'required': 'required',
        }),
        error_messages={
            'required': 'Telefon numarası zorunludur.'
        }
    )

    subject = forms.CharField(
        label='',
        required=False,  # Opsiyonel
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Konu (Opsiyonel)',
        })
    )

    message = forms.CharField(
        label='',
        min_length=10,
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Mesaj',
            'required': 'required',
            'rows': 12
        }),
        error_messages={
            'required': 'Mesaj alanı zorunludur.',
            'min_length': 'Mesaj en az 10 karakter olmalıdır.',
            'max_length': 'Mesaj en fazla 1000 karakter olabilir.'
        }
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        labels = {
            'name': 'İsim Soyisim',
            'email': 'E-posta',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Sadece harf, boşluk ve Türkçe karakterlere izin ver
            if not re.match(r'^[a-zA-ZçÇğĞıİöÖşŞüÜ\s]+$', name):
                raise ValidationError('İsim soyisim sadece harflerden oluşmalıdır.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Telefon numarasından sadece rakamları al
            digits_only = re.sub(r'\D', '', phone)
            if len(digits_only) < 10:
                raise ValidationError('Telefon numarası en az 10 rakam olmalıdır.')
        return phone

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            # Spam kontrolü - basit bir kontrol
            spam_words = ['spam', 'reklam', 'para kazan', 'tıkla']
            if any(word in message.lower() for word in spam_words):
                raise ValidationError('Mesajınız spam içerik barındırıyor olabilir.')
        return message

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        
        # E-posta veya telefon en az birisi dolu olmalı
        if not email and not phone:
            raise ValidationError('E-posta veya telefon numarasından en az birisi gereklidir.')
        
        return cleaned_data