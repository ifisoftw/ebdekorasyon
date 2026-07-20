from django.urls import path
from . views import ServicesView
from . import views

urlpatterns = [

    path('', ServicesView.as_view() , name="services"),
    
]