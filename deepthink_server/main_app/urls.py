from django.urls import path
from .views import TempClassView

urlpatterns = [
    path('test/', TempClassView.as_view(), name='test'),
]
