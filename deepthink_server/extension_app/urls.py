from django.urls import path
from .views import extension_view

urlpatterns = [
    path('naver_news/', extension_view, name='extension'),
]