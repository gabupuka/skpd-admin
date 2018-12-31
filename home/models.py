from django.db import models

class ATM(models.Model):
    id = models.CharField(max_length=7, primary_key=True)

    def __str__(self):
        return self.id

class SKPD(models.Model):
    atm                         = models.ForeignKey(ATM, on_delete=models.CASCADE)
    no_skpd                     = models.CharField(max_length=17, primary_key=True)
    nama_pemilik                = models.CharField(max_length=255)
    alamat_pemilik              = models.CharField(max_length=255)
    area_koordinasi_pemilik     = models.CharField(max_length=255)
    isi_teks                    = models.CharField(max_length=255)
    tempat_pemasangan           = models.CharField(max_length=255)
    lokasi_pemasangan           = models.CharField(max_length=255)
    kota_lokasi_pemasangan      = models.CharField(max_length=255)
    kecamatan_lokasi_pemasangan = models.CharField(max_length=255)
    kelurahan_lokasi_pemasangan = models.CharField(max_length=255)
    masa_berlaku_awal           = models.DateField()
    masa_berlaku_akhir          = models.DateField()
    nilai_sewa                  = models.IntegerField()
    comment                     = models.TextField()

    def __str__(self):
        return self.no_skpd

class Ukuran(models.Model):
    skpd        = models.OneToOneField(SKPD, on_delete=models.CASCADE, primary_key=True)
    panjang_1   = models.DecimalField(max_digits=3, decimal_places=2)
    lebar_1     = models.DecimalField(max_digits=3, decimal_places=2)
    panjang_2   = models.DecimalField(max_digits=3, decimal_places=2)
    lebar_2     = models.DecimalField(max_digits=3, decimal_places=2)
    panjang_3   = models.DecimalField(max_digits=3, decimal_places=2)
    lebar_3     = models.DecimalField(max_digits=3, decimal_places=2)
    panjang_4   = models.DecimalField(max_digits=3, decimal_places=2)
    lebar_4     = models.DecimalField(max_digits=3, decimal_places=2)
    total       = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return "%s - %sm" % (self.skpd, self.total)
