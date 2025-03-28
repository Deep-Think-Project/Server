from django.urls import path
from .views import home_view, home_view_async

urlpatterns = [
    path('', home_view, name='home'),
    # path('async/', home_view_async, name='home'),
]
