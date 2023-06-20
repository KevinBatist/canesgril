from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Prato
# Create your views here.

def index(request):
    pratos = Prato.objects.filter(publicado = True).order_by('-data_prato')
    contexto = {'lista_pratos' : pratos,}
    return render(request, 'index.html', contexto)
    # return HttpResponse('<h1>Churrasco - Canes Gril</h1><p>Toma o primeiro site<p>')

def churrasco(request, prato_id):
    # prato = Prato.objects.filter(pk = prato_id)
    prato = get_object_or_404(Prato, pk = prato_id)
    contexto = {'prato' : prato}
    return render(request, 'churrasco.html', contexto)