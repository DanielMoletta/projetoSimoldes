from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('projeto/<int:id_projeto>/', projeto_detail, name='projeto_detail'),
    path('projeto/<int:id_projeto>/editar/', editarProjeto, name='editar_projeto'),
    path('projeto/<int:id_projeto>/processo/<int:id_processo>/editar/', editar_processo, name='editar_processo'),
    path('projeto/<int:id_projeto>/processo/<int:id_processo>/editar/ferramenta/', editar_processo_ferramenta, name='editar_processo_ferramenta'),
    path('exportar-rubricas/', views.exportar_rubricas_excel, name='exportar_rubricas'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]