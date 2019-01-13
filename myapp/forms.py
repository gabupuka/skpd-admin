from django import forms

from .models import ATM, SKPD, Ukuran

class ATMCreateNewForm(forms.Form):
    atm_id                      = forms.CharField(label='ID ATM', max_length=7)
    no_skpd                     = forms.CharField(label='Nomor SKPD', max_length=17)
    nama_pemilik                = forms.CharField(label='Nama Pemilik Reklame', max_length=255)
    alamat_pemilik              = forms.CharField(label='Alamat', max_length=255)
    area_koordinasi_pemilik     = forms.CharField(label='Area Koordinasi', max_length=255)
    isi_teks                    = forms.CharField(label='Isi Teks Reklame', max_length=255)
    tempat_pemasangan           = forms.CharField(label='Tempat Pemasangan', max_length=255)
    lokasi_pemasangan           = forms.CharField(label='Lokasi Pemasangan', max_length=255)
    kota_lokasi_pemasangan      = forms.CharField(label='Kota', max_length=255)
    kecamatan_lokasi_pemasangan = forms.CharField(label='Kecamatan', max_length=255)
    kelurahan_lokasi_pemasangan = forms.CharField(label='Kelurahan', max_length=255)
    panjang_1                   = forms.DecimalField(label='Panjang', max_digits=3, decimal_places=2)
    lebar_1                     = forms.DecimalField(label='Lebar', max_digits=3, decimal_places=2)
    panjang_2                   = forms.DecimalField(label='Panjang', max_digits=3, decimal_places=2)
    lebar_2                     = forms.DecimalField(label='Lebar', max_digits=3, decimal_places=2)
    panjang_3                   = forms.DecimalField(label='Panjang', max_digits=3, decimal_places=2)
    lebar_3                     = forms.DecimalField(label='Lebar', max_digits=3, decimal_places=2)
    panjang_4                   = forms.DecimalField(label='Panjang', max_digits=3, decimal_places=2)
    lebar_4                     = forms.DecimalField(label='Lebar', max_digits=3, decimal_places=2)
    masa_berlaku_awal           = forms.DateField(label='Masa Pajak Reklame (Awal)')
    masa_berlaku_akhir          = forms.DateField(label='Masa Pajak Reklame (Akhir)')
    nilai_sewa                  = forms.IntegerField(label='Nilai Sewa Reklame')
