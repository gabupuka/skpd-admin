from django.db import models
from django.dispatch import receiver

from .storages import OverwriteStorage

import os

class ATM(models.Model):
    atm_id = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.id == None:
            return "ATM None"
        return self.atm_id

def skpd_pdf_file_path(instance, filename):
    return "pdf/ATM_{0}/SKPD_{1}/{2}".format(instance.atm.id, instance.id, filename)

class SKPD(models.Model):
    atm                         = models.ForeignKey(ATM, on_delete=models.CASCADE)
    no_skpd                     = models.CharField(max_length=17)
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
    pdf_file                    = models.FileField(storage=OverwriteStorage(), upload_to=skpd_pdf_file_path, default=None, blank=True, null=True)
    comment                     = models.TextField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id is None:
            saved_pdf_file = self.pdf_file
            self.pdf_file = None
            super(SKPD, self).save(*args, **kwargs)
            self.pdf_file = saved_pdf_file
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(SKPD, self).save(*args, **kwargs)

    def __str__(self):
        if self.no_skpd == None:
            return "SKPD None"
        return self.no_skpd

    def pdf_file_name(self):
        return os.path.basename(self.pdf_file.name)

@receiver(models.signals.post_delete, sender=SKPD)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.pdf_file:
        if os.path.isfile(instance.pdf_file.path):
            os.remove(instance.pdf_file.path)

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
