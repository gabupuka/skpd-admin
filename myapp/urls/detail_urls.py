from django.urls import path

from ..views import ATMDetailView, SKPDCreateNewView

app_name = 'myapp.detail_urls'
urlpatterns = [
    path('<int:pk>/', ATMDetailView.as_view(), name='detail'),
    path('<int:pk>/new-skpd/', SKPDCreateNewView.as_view(), name='create_new_skpd'),
]
