from django.urls import path

from ..views import ATMDetailView

app_name = 'myapp.detail_urls'
urlpatterns = [
    path('<int:pk>/', ATMDetailView.as_view(), name='detail'),
]
