from django.contrib import admin

# Register your models here.
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email','full_name','phone','created_at','company_name')
    search_fields = ('email','full_name')