from django.urls import path

from ..views import HomepageView, ATMCreateNewView

app_name = 'myapp.home_urls'
urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('new-atm/', ATMCreateNewView.as_view(), name='create_new_atm'),
]
