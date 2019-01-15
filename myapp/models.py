from django.db import models

class ATM(models.Model):
    atm_id = models.CharField(max_length=7, unique=True)

    def __str__(self):
        if self.id == None:
            return "ATM None"
        return self.atm_id

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
    comment                     = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        if self.no_skpd == None:
            return "SKPD None"
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

    @property
    def total(self):
        result = (self.panjang_1 * self.lebar_1) + (self.panjang_2 * self.lebar_2) + (self.panjang_3 * self.lebar_3) + (self.panjang_4 * self.lebar_4)
        return "%.2f" % result

    def __str__(self):
        return "%s - %sm" % (self.skpd, self.total)
