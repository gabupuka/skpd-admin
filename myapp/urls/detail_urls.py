from django.urls import path

from ..views import ATMDetailView, edit_ATM, SKPDCreateNewView, edit_SKPD

app_name = 'myapp.detail_urls'
urlpatterns = [
    path('<int:pk>/', ATMDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', edit_ATM, name='edit_atm'),
    path('<int:pk>/new-skpd/', SKPDCreateNewView.as_view(), name='create_new_skpd'),
    path('<int:pk>/edit-skpd/<str:no_skpd>/', edit_SKPD, name='edit_skpd'),
]
