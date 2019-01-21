from django.urls import path

from ..views import ATMDetailView, edit_ATM, delete_ATM, SKPDCreateNewView, edit_SKPD, delete_SKPD

app_name = 'myapp.detail_urls'
urlpatterns = [
    path('<int:pk>/', ATMDetailView.as_view(), name='detail'),
    path('<int:pk>/edit-atm', edit_ATM, name='edit_atm'),
    path('<int:pk>/delete-atm', delete_ATM, name='delete_atm'),
    path('<int:pk>/new-skpd/', SKPDCreateNewView.as_view(), name='create_new_skpd'),
    path('<int:pk>/skpd/<str:no_skpd>/edit-skpd/', edit_SKPD, name='edit_skpd'),
    path('<int:pk>/skpd/<str:no_skpd>/delete-skpd/', delete_SKPD, name='delete_skpd'),
]
