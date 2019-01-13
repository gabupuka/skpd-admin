from django.urls import path

from ..views import HomepageView

app_name = 'myapp.home_urls'
urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
]
