from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout


from app_simoldes.forms import LoginForm, RegistrationForm
from .models import Processo
from .models import Projeto

def login_view(request):
    if request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                username = User.objects.get(email=email).username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect(request.GET.get('next', 'home'))
                else:
                    form.add_error(None, 'Email ou senha incorretos')
            except User.DoesNotExist:
                form.add_error('email', 'Email não registrado')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'processos': Processo.objects.all(),
        'projetos': Projeto.objects.all(),
    }

    return render(request, 'home.html', context)