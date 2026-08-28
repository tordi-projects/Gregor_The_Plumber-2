from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.service_list, name='service_list'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('contact/', views.contact, name='contact'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/<int:pk>/', views.staff_quote_detail, name='staff_quote_detail'),
]
