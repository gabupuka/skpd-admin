from django.urls import path

from ..views import ATMDetailView, edit_ATM, SKPDCreateNewView, edit_SKPD, download_pdf_file

app_name = 'myapp.detail_urls'
urlpatterns = [
    path('<int:pk>', ATMDetailView.as_view(), name='detail'),
    path('<int:pk>/edit-atm', edit_ATM, name='edit_atm'),
    path('<int:pk>/new-skpd', SKPDCreateNewView.as_view(), name='create_new_skpd'),
    path('<int:pk>/skpd/<int:pk_skpd>/edit-skpd', edit_SKPD, name='edit_skpd'),
    path('<int:pk>/skpd/<int:pk_skpd>/download/<str:file_name>', download_pdf_file, name='download_pdf_file'),
]
