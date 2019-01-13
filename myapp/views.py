from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import ATM, SKPD, Ukuran

class HomepageView(generic.ListView):
    template_name = 'myapp/homepage.html'
    context_object_name = 'homepage_list'

    def get_queryset(self):
        atm_list = ATM.objects.order_by('-id')[:10]
        result_list = []

        for atm in atm_list:
            skpd = atm.skpd_set.order_by('-masa_berlaku_akhir')[0]
            ukuran_skpd = Ukuran.objects.get(skpd=skpd)
            result_item = (skpd, ukuran_skpd)
            result_list.append(result_item)

        return result_list

class ATMDetailView(generic.DetailView):
    model = ATM
    template_name = 'myapp/atm_detail.html'
    context_object_name = 'atm_detail'

    def get_object(self):
        atm = super().get_object()
        skpd_list = SKPD.objects.filter(atm=atm).order_by('masa_berlaku_akhir')
        result_object = {
            'tempat_pemasangan': skpd_list[0].tempat_pemasangan,
            'lokasi_pemasangan': skpd_list[0].lokasi_pemasangan,
            'atm_id': atm.atm_id,
            'skpd_list': skpd_list
        }

        return result_object
