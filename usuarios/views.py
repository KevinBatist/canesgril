from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from churras.models import Prato

def cadastro(request):
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']

        if not nome.strip():
            return redirect('cadastro')
        if not email.strip():
            return redirect('cadastro')
        if senha != senha2 or not senha.strip() or not senha2.strip():
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        return redirect("login")
    
    return render(request, 'cadastro.html')

def login(request):
    if request.method =="POST":
        email = request.POST['email'].strip()
        senha = request.POST['senha'].strip()

        if email == "" or senha == "":
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username = nome, password=senha)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            

    return render(request, 'login.html')

def dashboard(request):
    pratos = Prato.objects.filter(publicado = True).order_by('-data_prato')
    contexto = {'lista_pratos' : pratos,}

    if request.user.is_authenticated:
        return render(request, 'dashboard.html', contexto)
    return redirect('index')




def logout(request):
    auth.logout(request)
    return redirect('index')

def criar_prato(request):
    if request.method == "POST":
        nome_prato = request.POST['nome_prato']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_prato = request.POST['foto_prato']


    return render(request, 'criar_prato.html')