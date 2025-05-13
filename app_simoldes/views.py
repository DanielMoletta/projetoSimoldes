from django.shortcuts import render
from .models import Processo
from .models import Projeto

def home(request):
    context = {
        'processos': Processo.objects.all(),
        'projetos': Projeto.objects.all(),
    }

    return render(request, 'home.html', context)