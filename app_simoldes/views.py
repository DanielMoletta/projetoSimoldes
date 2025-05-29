from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from .forms import ProcessoEditForm


from app_simoldes.forms import *
from .models import Processo, Projeto

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
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def home(request):
    # 1. Busca projetos que têm TODOS os processos com rubrica=True E rubrica_montador=True
    projetos_concluidos = Projeto.objects.annotate(
        total_processos=Count('processo'),
        rubricas_ok=Count('processo', filter=Q(processo__rubrica=True) & Q(processo__rubrica_montador=True))
    ).filter(
        total_processos__gt=0,  # Exclui projetos sem processos
        rubricas_ok=F('total_processos')  # Todos os processos devem estar OK
    )

    # 2. Busca projetos PENDENTES (pelo menos um processo não está rubricado)
    projetos_pendentes = Projeto.objects.exclude(
        id__in=projetos_concluidos.values('id')
    )

    # 3. Projeto atual = primeiro projeto pendente (se houver)
    projeto_atual = projetos_pendentes.first()

    # 4. Se não houver pendentes, pega o último concluído (opcional)
    if not projeto_atual:
        projeto_atual = projetos_concluidos.order_by('-id').first()

    # 5. Verificação final (redundante, mas segura)
    projeto_completo = False
    processos = []
    if projeto_atual:
        processos = projeto_atual.processo_set.all()
        projeto_completo = all(p.rubrica and p.rubrica_montador for p in processos)

    context = {
        'projeto': projeto_atual,
        'processos': processos,
        'projeto_completo': projeto_completo,
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    projetos = Projeto.objects.all()
    return render(request, 'dashboard.html', {'projetos': projetos})

@login_required
def projeto_detail(request, id_projeto):
    projeto = get_object_or_404(Projeto, id=id_projeto)
    processos = Processo.objects.filter(projeto=projeto)
    return render(request, 'projeto_detail.html', {
        'projeto': projeto,
        'processos': processos,
    })

@login_required
def editarProjeto(request, id_projeto):
    projeto = get_object_or_404(Projeto, id=id_projeto)
    if request.method == 'POST':
        form = ProjetoEditForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            
            return redirect('home')
    else:
        form = ProjetoEditForm(instance=projeto)
    return render(request, 'editar_projeto.html', {
        'form': form,
        'projeto_id': id_projeto
    })

@login_required
def editar_processo(request, id_projeto, id_processo):
    processo = get_object_or_404(Processo, id=id_processo, projeto__id=id_projeto)

    if request.method == 'POST':
        form = ProcessoEditForm(request.POST, instance=processo)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProcessoEditForm(instance=processo)

    return render(request, 'editar_processo.html', {
        'form': form,
        'projeto_id': id_projeto,
        'processo': processo,
    })

@login_required
def editar_processo_ferramenta(request, id_projeto, id_processo):
    processo = get_object_or_404(Processo, id=id_processo, projeto__id=id_projeto)

    if request.method == 'POST':
        form = ProcessoFerramentaEditForm(request.POST, instance=processo)
        if form.is_valid():
            # salva a rubrica_montador (True ou False)
            form.save()
            return redirect('home')
    else:
        form = ProcessoFerramentaEditForm(instance=processo)

    return render(request, 'editar_processo_ferramenta.html', {
        'form': form,
        'projeto_id': id_projeto,
        'processo': processo,
    })