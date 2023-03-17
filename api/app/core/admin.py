"""
Django admin customization.
"""
from django.contrib import admin

from core import models
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple


class BitFieldModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


admin.site.register(models.Place)
admin.site.register(models.Setting, BitFieldModelAdmin)
admin.site.register(models.Event)
