from django.urls import path
from . views import IndexView, AboutView, ContactView, FaqView, PrivacyPolicyView, TermsOfServiceView, KvkkView, robots_txt
from service import views as service_view
from service.views import  ServicesView, ServiceAreaListView
from blog.views import BlogListView, BlogDetailView

urlpatterns = [
    path('', IndexView.as_view(), name="index" ),
    path('hakkimizda/', AboutView.as_view(), name="about" ),
    path('iletisim/', ContactView.as_view(), name="contact" ),
    path('hizmetler/', ServicesView.as_view(),name='services'),
    path('hizmet-bolgeleri/', ServiceAreaListView.as_view(), name='service_areas'),
    path('bloglar/', BlogListView.as_view(),name='blogs'),
    path('bloglar/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('sss/', FaqView.as_view(),name='faqs'),
    # Yasal Sayfalar
    path('gizlilik-politikasi/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('kullanim-sartlari/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('kvkk/', KvkkView.as_view(), name='kvkk'),
    path('<slug:slug>/',service_view.service_detail , name='service_detail'),
    
    # Search Console URLs
    path('robots.txt', robots_txt, name='robots_txt'),
]
