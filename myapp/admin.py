from django.contrib import admin

from .models import ATM, SKPD, Ukuran

class SKPDInline(admin.TabularInline):
    model = SKPD
    extra = 2

class ATMAdmin(admin.ModelAdmin):
    inlines = [SKPDInline]
    list_display = ('id', 'atm_id')

class SKPDAdmin(admin.ModelAdmin):
    list_display = ('id', 'no_skpd', 'masa_berlaku_awal', 'masa_berlaku_akhir', 'atm_id')

admin.site.register(ATM, ATMAdmin)
admin.site.register(SKPD, SKPDAdmin)
admin.site.register(Ukuran)
