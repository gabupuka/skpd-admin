from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from myapp.forms import ATMForm, SKPDForm

from .models import ATM, SKPD, Ukuran
from .templatetags.myapp_extras import in_group

import json

class HomepageView(LoginRequiredMixin, generic.ListView):
    template_name = 'myapp/homepage.html'
    context_object_name = 'homepage_list'
    redirect_field_name = None

    def get_queryset(self):
        atm_list = ATM.objects.order_by('-id')
        result_list = []

        for atm in atm_list:
            skpd = atm.skpd_set.order_by('-masa_berlaku_akhir')[0]
            ukuran_skpd = Ukuran.objects.get(skpd=skpd)
            result_item = (atm, skpd, ukuran_skpd)
            result_list.append(result_item)

        return result_list

class ATMDetailView(LoginRequiredMixin, generic.DetailView):
    model = ATM
    template_name = 'myapp/atm_detail.html'
    context_object_name = 'atm_detail'
    redirect_field_name = None

    def get_object(self):
        atm = super().get_object()
        skpd_list = SKPD.objects.filter(atm=atm).order_by('masa_berlaku_akhir')
        latest_skpd_idx = len(skpd_list)-1
        result_object = {
            'tempat_pemasangan': skpd_list[latest_skpd_idx].tempat_pemasangan,
            'lokasi_pemasangan': skpd_list[latest_skpd_idx].lokasi_pemasangan,
            'atm_id': atm.atm_id,
            'atm_pk': atm.id,
            'skpd_list': skpd_list,
            'is_active': atm.is_active
        }

        return result_object

    # Delete ATM or SKPD
    def post(self, request, pk):
        if request.POST.get("yes_button"):
            if request.POST['type'] == 'SKPD':
                skpd = SKPD.objects.get(pk=request.POST['value'])
                skpd.delete()
                return redirect(reverse('myapp.detail_urls:detail', args=(pk,)))
            elif request.POST['type'] == 'ATM':
                atm = ATM.objects.get(pk=request.POST['value'])
                atm.delete()
                return redirect(reverse('myapp.home_urls:homepage'))
            else:
                atm = ATM.objects.get(pk=request.POST['value'])
                atm.is_active = json.loads(request.POST['boolean'])
                atm.save()
                return redirect(reverse('myapp.detail_urls:detail', args=(pk,)))

class ATMCreateNewView(LoginRequiredMixin, generic.FormView):
    form_class = ATMForm
    template_name = 'myapp/atm_form.html'
    success_url = reverse_lazy('myapp.home_urls:homepage')
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        kwargs['title_prefix'] = "Tambah ATM Baru"
        return super().get_context_data(**kwargs)

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
        skpd.pdf_file = self.request.FILES.get('pdf_file', skpd.pdf_file)
        skpd.image_file = self.request.FILES.get('image_file', skpd.image_file)
        skpd.comment = data.get('comment')
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

    def get(self, request):
        if not in_group(request.user, 'Admin'):
            return redirect(reverse('myapp.home_urls:homepage'))
        else:
            return super().get(request)

def edit_ATM(request, pk):
    if not request.user.is_authenticated:
        return redirect(reverse('custom_login'))
    elif not in_group(request.user, 'Admin'):
        return redirect(reverse('myapp.home_urls:homepage'))
    else:
        atm = ATM.objects.get(pk=pk)
        skpd_list = SKPD.objects.filter(atm=atm).order_by('masa_berlaku_akhir')
        latest_skpd_idx = len(skpd_list)-1
        skpd = skpd_list[latest_skpd_idx]

        def get_ATM_with_latest_SKPD_data():
            return {
                'atm_id': atm.atm_id,
                'no_skpd': skpd.no_skpd,
                'nama_pemilik': skpd.nama_pemilik,
                'alamat_pemilik': skpd.alamat_pemilik,
                'area_koordinasi_pemilik': skpd.area_koordinasi_pemilik,
                'isi_teks': skpd.isi_teks,
                'tempat_pemasangan': skpd.tempat_pemasangan,
                'lokasi_pemasangan': skpd.lokasi_pemasangan,
                'kota_lokasi_pemasangan': skpd.kota_lokasi_pemasangan,
                'kecamatan_lokasi_pemasangan': skpd.kecamatan_lokasi_pemasangan,
                'kelurahan_lokasi_pemasangan': skpd.kelurahan_lokasi_pemasangan,
                'panjang_1': skpd.ukuran.panjang_1,
                'lebar_1': skpd.ukuran.lebar_1,
                'panjang_2': skpd.ukuran.panjang_2,
                'lebar_2': skpd.ukuran.lebar_2,
                'panjang_3': skpd.ukuran.panjang_3,
                'lebar_3': skpd.ukuran.lebar_3,
                'panjang_4': skpd.ukuran.panjang_4,
                'lebar_4': skpd.ukuran.lebar_4,
                'masa_berlaku_awal': skpd.masa_berlaku_awal,
                'masa_berlaku_akhir': skpd.masa_berlaku_akhir,
                'nilai_sewa': skpd.nilai_sewa,
                'pdf_file': skpd.pdf_file,
                'image_file': skpd.image_file,
                'comment': skpd.comment
            }

        def edit_ATM_with_latest_SKPD(atm, skpd, data):
            atm.atm_id = data.get('atm_id')
            atm.save()

            skpd.no_skpd = data.get('no_skpd')
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
            skpd.pdf_file = request.FILES.get('pdf_file', skpd.pdf_file)
            skpd.image_file = request.FILES.get('image_file', skpd.image_file)
            skpd.comment = data.get('comment')
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

        # Submit form
        if request.method == 'POST':
            form = ATMForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                edit_ATM_with_latest_SKPD(atm, skpd, data)

                return redirect(reverse('myapp.detail_urls:detail', args=(pk,)))

        # Show initial view
        else:
            initial_data = get_ATM_with_latest_SKPD_data()
            form = ATMForm(initial=initial_data)

        context = {
            'title_prefix': "Ubah ATM",
            'form': form,
            'atm_id': atm.atm_id
        }

        return render(request, 'myapp/atm_form.html', context)

class SKPDCreateNewView(LoginRequiredMixin, generic.FormView):
    form_class = SKPDForm
    template_name = 'myapp/skpd_form.html'
    redirect_field_name = None

    def get_atm_detail_context(self):
        atm = ATM.objects.get(pk=self.kwargs['pk'])
        skpd = SKPD.objects.filter(atm=atm)[0]
        context = {
            'tempat_pemasangan': skpd.tempat_pemasangan,
            'lokasi_pemasangan': skpd.lokasi_pemasangan,
            'atm_id': atm.atm_id
        }

        return context

    def get_context_data(self, **kwargs):
        kwargs['title_prefix'] = "Tambah SKPD Baru"
        kwargs['atm_detail'] = self.get_atm_detail_context()
        return super().get_context_data(**kwargs)

    def create_new_SKPD(self, data):
        atm = ATM.objects.get(pk=self.kwargs['pk'])

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
        skpd.pdf_file = self.request.FILES.get('pdf_file', skpd.pdf_file)
        skpd.image_file = self.request.FILES.get('image_file', skpd.image_file)
        skpd.comment = data.get('comment')
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
        self.create_new_SKPD(data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('myapp.detail_urls:detail', args=(self.kwargs['pk'],))
    
    def get(self, request, *args, **kwargs):
        if not in_group(request.user, 'Admin'):
            return redirect(reverse('myapp.home_urls:homepage'))
        else:
            return super().get(request, *args, **kwargs)

def edit_SKPD(request, pk, pk_skpd):
    if not request.user.is_authenticated:
        return redirect(reverse('custom_login'))
    elif not in_group(request.user, 'Admin'):
        return redirect(reverse('myapp.home_urls:homepage'))
    else:
        skpd = SKPD.objects.get(pk=pk_skpd)

        def get_SKPD_data():
            return {
                'no_skpd': skpd.no_skpd,
                'nama_pemilik': skpd.nama_pemilik,
                'alamat_pemilik': skpd.alamat_pemilik,
                'area_koordinasi_pemilik': skpd.area_koordinasi_pemilik,
                'isi_teks': skpd.isi_teks,
                'tempat_pemasangan': skpd.tempat_pemasangan,
                'lokasi_pemasangan': skpd.lokasi_pemasangan,
                'kota_lokasi_pemasangan': skpd.kota_lokasi_pemasangan,
                'kecamatan_lokasi_pemasangan': skpd.kecamatan_lokasi_pemasangan,
                'kelurahan_lokasi_pemasangan': skpd.kelurahan_lokasi_pemasangan,
                'panjang_1': skpd.ukuran.panjang_1,
                'lebar_1': skpd.ukuran.lebar_1,
                'panjang_2': skpd.ukuran.panjang_2,
                'lebar_2': skpd.ukuran.lebar_2,
                'panjang_3': skpd.ukuran.panjang_3,
                'lebar_3': skpd.ukuran.lebar_3,
                'panjang_4': skpd.ukuran.panjang_4,
                'lebar_4': skpd.ukuran.lebar_4,
                'masa_berlaku_awal': skpd.masa_berlaku_awal,
                'masa_berlaku_akhir': skpd.masa_berlaku_akhir,
                'nilai_sewa': skpd.nilai_sewa,
                'pdf_file': skpd.pdf_file,
                'image_file': skpd.image_file,
                'comment': skpd.comment
            }

        def edit_SKPD(skpd, data):
            skpd.no_skpd = data.get('no_skpd')
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
            skpd.pdf_file = request.FILES.get('pdf_file', skpd.pdf_file)
            skpd.image_file = request.FILES.get('image_file', skpd.image_file)
            skpd.comment = data.get('comment')
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

        # Submit form
        if request.method == 'POST':
            form = SKPDForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                edit_SKPD(skpd, data)

                return redirect(reverse('myapp.detail_urls:detail', args=(pk,)))

        # Show initial view
        else:
            initial_data = get_SKPD_data()
            form = SKPDForm(initial=initial_data)

        context = {
            'title_prefix': "Ubah SKPD",
            'atm_detail': {
                'tempat_pemasangan': skpd.tempat_pemasangan,
                'lokasi_pemasangan': skpd.lokasi_pemasangan,
                'atm_id': skpd.atm.atm_id                
            },
            'form': form,
            'no_skpd': skpd.no_skpd
        }

        return render(request, 'myapp/skpd_form.html', context)

def download_pdf_file(request, pk, pk_skpd, file_name):
    if not request.user.is_authenticated:
        return redirect(reverse('custom_login'))
    else:
        skpd = SKPD.objects.get(pk=pk_skpd)

        response = HttpResponse(skpd.pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=%s' % file_name

        return response

def download_image_file(request, pk, pk_skpd, file_name):
    if not request.user.is_authenticated:
        return redirect(reverse('custom_login'))
    else:
        skpd = SKPD.objects.get(pk=pk_skpd)

        image_data = open(skpd.image_file.path, "rb").read()
        response = HttpResponse(image_data, content_type='image/jpeg')
        response['Content-Disposition'] = 'inline; filename=%s' % file_name

        return response
