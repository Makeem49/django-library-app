from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-name'),
    path('frequent-questions', views.faq, name='blog-faq'),
    path('about', views.about, name='blog-about')
]

