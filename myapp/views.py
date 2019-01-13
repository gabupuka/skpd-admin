from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from myapp.forms import ATMCreateNewForm

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

class ATMCreateNewView(generic.FormView):
    form_class = ATMCreateNewForm
    template_name = 'myapp/atm_create_new.html'
    success_url = reverse_lazy('myapp.home_urls:homepage')

    def create_new_ATM(self, data):
        atm = ATM(atm_id=data.get('atm_id'))
        atm.save()

        skpd = SKPD(atm=atm, no_skpd=data.get('no_skpd'))
        skpd.nama_pemilik = data.get('nama_pemilik')
        skpd.alamat_pemilik = data.get('alamat_pemilik')
        skpd.area_koordinasi_pemilik = data.get('area_koordinasi_pemilik')
        skpd.isi_teks = data.get('isi_teks')
        skpd.tempat_pemasangan = data.get('tempat_pemasangan')
        skpd.lokasi_pemasangan = data.get('lokasi_pemasangan')
        skpd.kota_lokasi_pemasangan = data.get('kota_lokasi_pemasangan')
        skpd.kecamatan_lokasi_pemasangan = data.get('kecamatan_lokasi_pemasangan')
        skpd.kelurahan_lokasi_pemasangan = data.get('kelurahan_lokasi_pemasangan')
        skpd.masa_berlaku_awal = data.get('masa_berlaku_awal')
        skpd.masa_berlaku_akhir = data.get('masa_berlaku_akhir')
        skpd.nilai_sewa = data.get('nilai_sewa')
        skpd.save()

        ukuran = Ukuran(skpd=skpd)
        ukuran.panjang_1 = data.get('panjang_1')
        ukuran.lebar_1 = data.get('lebar_1')
        ukuran.panjang_2 = data.get('panjang_2')
        ukuran.lebar_2 = data.get('lebar_2')
        ukuran.panjang_3 = data.get('panjang_3')
        ukuran.lebar_3 = data.get('lebar_3')
        ukuran.panjang_4 = data.get('panjang_4')
        ukuran.lebar_4 = data.get('lebar_4')
        ukuran.save()

    def form_valid(self, form):
        data = form.cleaned_data
        self.create_new_ATM(data)
        return super().form_valid(form)
