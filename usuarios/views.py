from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

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
    return render(request, 'dashboard.html')





def logout(request):
    auth.logout(request)
    return redirect('index')