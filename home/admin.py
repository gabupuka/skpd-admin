from django.contrib import admin

from .models import ATM, SKPD, Ukuran

class SKPDInline(admin.StackedInline):
    model = SKPD
    extra = 1

class ATMAdmin(admin.ModelAdmin):
    inlines = [SKPDInline]

admin.site.register(ATM, ATMAdmin)
admin.site.register(SKPD)
admin.site.register(Ukuran)
