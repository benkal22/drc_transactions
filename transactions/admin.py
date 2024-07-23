from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Product)
admin.site.register(Producer)
admin.site.register(Client)
admin.site.register(Supplier)
admin.site.register(Transaction)
admin.site.register(UniqueSector)
# admin.site.register(ProducerClient)
# admin.site.register(ProducerSupplier)
