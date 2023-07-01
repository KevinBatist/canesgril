from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from churras.models import Prato


def campo_vazio(campo):
    return not campo.strip()
def senha_diferente(senha, senha2):
    return senha != senha2 or campo_vazio(senha) or campo_vazio(senha2)


def cadastro(request):
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['senha']
        senha2 = request.POST['senha2']

        if campo_vazio(nome):
            messages.error(request, "Existem campos vazios, preencha todos eles")
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, "Existem campos vazios, preencha todos eles")
            return redirect('cadastro')
        if senha_diferente(senha, senha2):
            messages.error(request, "As senhas digitadas não sao iguais")
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, "E-mail já cadastrado")
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
            messages.error(request, 'Os campos e-mail e senha devem ser preenchidos')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username = nome, password=senha)
            

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('dashboard')
            
        messages.error(request, 'Usuário e/ou senha incorretos')
    return render(request, 'login.html')

def dashboard(request):
    pratos = Prato.objects.filter(pessoa=request.user.id).order_by('-data_prato')
    contexto = {'lista_pratos' : pratos,}

    if request.user.is_authenticated:
        return render(request, 'dashboard.html', contexto)
    messages.success(request, "Você nao tem autorização para acessar o dashboard, faça login")
    return redirect('index')




def logout(request):
    auth.logout(request)
    return redirect('index')

def criar_prato(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            nome_prato = request.POST['nome_prato']
            ingredientes = request.POST['ingredientes']
            modo_preparo = request.POST['modo_preparo']
            tempo_preparo = request.POST['tempo_preparo']
            rendimento = request.POST['rendimento']
            categoria = request.POST['categoria']
            foto_prato = request.POST['foto_prato']

            user = get_object_or_404(User, pk=request.user.id)
            prato = Prato.objects.create(pessoa=user, 
                                        nome_prato=nome_prato, 
                                        ingredientes=ingredientes,
                                        modo_preparo=modo_preparo, 
                                        tempo_preparo=tempo_preparo,
                                        rendimento=rendimento,
                                        categoria=categoria,
                                        foto_prato=foto_prato,
                                        )
            prato.save()
            messages.success(request, "Prato criado com sucesso!")
            return redirect('dashboard')
    
        return render(request, 'criar_prato.html')
    
    messages.error(request, "Você nao tem autorização para criar pratos")
    return redirect('index')