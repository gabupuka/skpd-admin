from django.contrib import admin

from .models import ATM, SKPD, Ukuran

class SKPDInline(admin.TabularInline):
    model = SKPD
    extra = 2

class ATMAdmin(admin.ModelAdmin):
    inlines = [SKPDInline]

class SKPDAdmin(admin.ModelAdmin):
    list_display = ('atm_id', 'no_skpd', 'masa_berlaku_awal', 'masa_berlaku_akhir')

admin.site.register(ATM, ATMAdmin)
admin.site.register(SKPD, SKPDAdmin)
admin.site.register(Ukuran)
