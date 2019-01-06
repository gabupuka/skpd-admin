from django.urls import path

from .. import views

app_name = 'myapp.detail_urls'
urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
]
