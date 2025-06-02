from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
import matplotlib
from .forms import ProcessoEditForm
import datetime
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from openpyxl import Workbook
import os
from django.conf import settings
from django.shortcuts import render
from openpyxl import Workbook

import matplotlib.pyplot as plt

matplotlib.use('Agg')

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
    # 1) Obter contagens reais dos seus models
    total_rubrica_true = Processo.objects.filter(rubrica=True).count()
    total_rubrica_false = Processo.objects.filter(rubrica=False).count()

    total_rm_true = Processo.objects.filter(rubrica_montador=True).count()
    total_rm_false = Processo.objects.filter(rubrica_montador=False).count()

    projetos_concluidos = Projeto.objects.annotate(
        total_processos=Count('processo'),
        rubricas_ok=Count('processo', filter=Q(processo__rubrica=True) & Q(processo__rubrica_montador=True))
    ).filter(total_processos__gt=0, rubricas_ok=F('total_processos')).count()
    projetos_pendentes = Projeto.objects.count() - projetos_concluidos

    # 2) Criar / garantir diretório para salvar gráficos
    charts_dir = os.path.join(settings.BASE_DIR, 'static', 'charts')
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)

    # 3) Aplica style “ggplot” (ou outro de sua preferência) para visual limpo
    plt.style.use('ggplot')

    # 4) Gráfico de barras para Rúbrica
    plt.figure(figsize=(6, 4))
    labels_rt = ['Rubricados', 'Não Rubricados']
    values_rt = [total_rubrica_true, total_rubrica_false]
    plt.bar(labels_rt, values_rt, color=["#00A785", "#B6B6B6"], edgecolor='black', linewidth=1.2)
    plt.title('', fontsize=16, fontweight='bold')
    plt.ylabel('Quantidade', fontsize=12)
    plt.xlabel('Status da Rúbrica', fontsize=12)
    for i, v in enumerate(values_rt):
        plt.text(i, v + max(values_rt) * 0.02, str(v),
                 ha='center', fontsize=12, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    path_rubrica = os.path.join(charts_dir, 'styled_rubrica_chart.png')
    plt.savefig(path_rubrica)
    plt.close()

    # 5) Gráfico de barras para Rúbrica Montador
    plt.figure(figsize=(6, 4))
    labels_rm = ['Rubricados Montador', 'Não Rubricados Montador']
    values_rm = [total_rm_true, total_rm_false]
    plt.bar(labels_rm, values_rm, color=['#00A785', '#B6B6B6'], edgecolor='black', linewidth=1.2)
    plt.title('', fontsize=16, fontweight='bold')
    plt.ylabel('Quantidade', fontsize=12)
    plt.xlabel('Status da Rúbrica Montador', fontsize=12)
    for i, v in enumerate(values_rm):
        plt.text(i, v + max(values_rm) * 0.02, str(v),
                 ha='center', fontsize=12, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    path_rm = os.path.join(charts_dir, 'styled_rubrica_montador_chart.png')
    plt.savefig(path_rm)
    plt.close()

    # 6) Gráfico de barras para Projetos concl. vs pendentes
# 6) Gráfico de pizza para Projetos concl. vs pendentes
    plt.figure(figsize=(6, 6))  # Pizza normalmente fica melhor em formato quadrado
    labels_proj = ['Concluídos', 'Pendentes']
    values_proj = [projetos_concluidos, projetos_pendentes]
    colors = ['#00A785', '#B6B6B6']

    plt.pie(
        values_proj,
        labels=labels_proj,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )

    plt.title('', fontsize=16, fontweight='bold')
    plt.axis('equal')  # Mantém o círculo redondo (mesmo se a figura for retangular)

    path_proj = os.path.join(charts_dir, 'styled_project_status_chart.png')
    plt.savefig(path_proj)
    plt.close()

    # 7) Montar contexto com URLs relativas às imagens
    context = {
        'projetos': Projeto.objects.all(),
        'chart_rubrica_url': 'charts/styled_rubrica_chart.png',
        'chart_rubrica_montador_url': 'charts/styled_rubrica_montador_chart.png',
        'chart_project_status_url': 'charts/styled_project_status_chart.png',
    }
    return render(request, 'dashboard.html', context)

@login_required
def projeto_detail(request, id_projeto):
    projeto = get_object_or_404(Projeto, id=id_projeto)

    # Aqui está o fix: select_related com os campos relacionados ao User
    processos = Processo.objects.select_related('rubrica_user', 'rubrica_montador_user').filter(projeto=projeto)

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

@login_required
def confirmar_rubrica(request, projeto_id, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)

    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
        tipo = request.POST.get('tipo')  # rubrica ou rubrica_montador
        user = authenticate(username=matricula, password=senha)

        if user is not None:
            if tipo == 'rubrica':
                processo.rubrica = True
                processo.rubrica_user = user
                messages.success(request, f'Rúbrica confirmada por {user.get_full_name()}')
            elif tipo == 'rubrica_montador':
                processo.rubrica_montador = True
                processo.rubrica_montador_user = user
                messages.success(request, f'Rúbrica do montador confirmada por {user.get_full_name()}')
            else:
                messages.error(request, 'Tipo de rúbrica inválido')
                return redirect('projeto_detail', projeto_id=projeto_id)

            processo.save()
        else:
            messages.error(request, 'Matrícula ou senha inválidos')

    return redirect('projeto_detail', projeto_id=projeto_id)

@login_required
def exportar_rubricas_excel(request):
    """
    Gera um arquivo Excel (.xlsx) contendo todos os LogEntry relacionados
    a mudanças de rubrica (tanto rubrica quanto rubrica_montador) do modelo Processo.
    """

    # 1. Identificar o ContentType de Processo
    ct_processo = ContentType.objects.get_for_model(Processo)

    # 2. Filtrar LogEntry apenas do conteúdo "Processo" e que contenham 'rubrica'
    #    no change_message. Assim só pegamos os logs de mudanças de rubrica.
    logs = LogEntry.objects.filter(
        content_type=ct_processo,
        change_message__icontains="rubrica"
    ).order_by('action_time')

    # 3. Criar workbook do openpyxl
    wb = Workbook()
    ws = wb.active
    ws.title = "Logs de Rúbrica"

    # 4. Cabeçalho
    ws.append([
        "Data/Hora",      # action_time
        "Usuário",        # usuário que fez a ação
        "ID do Objeto",   # object_id (Processo.id)
        "Representação",  # object_repr (string do objeto)
        "Mensagem de Mudança"  # change_message
    ])

    # 5. Preencher linhas com cada LogEntry encontrado
    for entry in logs:
        # formata data/hora como string legível
        ts = entry.action_time.strftime("%Y-%m-%d %H:%M:%S")
        # usuário: entry.user pode ser None (mas geralmente estará preenchido)
        user_str = entry.user.get_full_name() or entry.user.username if entry.user else "—"
        ws.append([
            ts,
            user_str,
            entry.object_id,
            entry.object_repr,
            entry.change_message,
        ])

    # 6. Preparar resposta HTTP com o Excel gerado em memória
    nome_arquivo = f"rubricas_{datetime.date.today().strftime('%Y%m%d')}.xlsx"
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{nome_arquivo}"'

    # 7. Gravar o workbook no HttpResponse
    wb.save(response)
    return response