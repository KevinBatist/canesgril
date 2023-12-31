from django.contrib import admin
from .models import Pessoa
# Register your models here.

class ListandoPessoas(admin.ModelAdmin):
    list_display = ['id', 'nome', 'email']
    list_display_links = ['id', 'nome']
    ordering = ['-id']
    list_per_page = 5

admin.site.register(Pessoa, ListandoPessoas)