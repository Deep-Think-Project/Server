from django.urls import path
from .views import home_view, gemini_view

urlpatterns = [
    path('', home_view, name='home'),
    path('gemini/', gemini_view, name='gemini'),
]
