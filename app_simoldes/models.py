from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Projeto(models.Model):
    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    id = models.AutoField(primary_key=True)
    maquina = models.CharField(max_length=100)
    data = models.DateField(auto_now=False, auto_now_add=False)
    pasta_programas = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    programador = models.CharField(max_length=100)
    aperto = models.CharField(max_length=100)
    tempo_projeto = models.CharField(max_length=100)
    centro_bloco = models.CharField(max_length=100)
    referencia_z = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='media/', blank=True, null=True)
    observacao = models.CharField(max_length=100)
    setup_inicio = models.DateField(blank=True, null=True)
    setup_hora_ini = models.DurationField(blank=True, null=True)
    setup_termino = models.DateField(blank=True, null=True)
    setup_hora_ter = models.DurationField(blank=True, null=True)
    usina_inicio = models.DateField(blank=True, null=True)
    usina_hora_ini = models.DurationField(blank=True, null=True)
    usina_termino = models.DateField(blank=True, null=True)
    usina_hora_ter = models.DurationField(blank=True, null=True)

    def esta_concluido(self):
        """Verifica se todos os processos do projeto estão rubricados."""
        return not self.processo_set.filter(rubrica=False).exists()

    def marcar_como_concluido(self):
        """Marca o projeto como concluído se todos os processos estiverem rubricados."""
        if self.esta_concluido():
            # Você pode adicionar um campo 'concluido' ou fazer outra ação
            pass

    def __str__(self):
        return f"Programa - {self.id}"

class Processo(models.Model):
    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
     
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    id = models.AutoField(primary_key=True)
    programa = models.CharField(max_length=100)
    tipo_percurso = models.CharField(max_length=100)
    referencia = models.CharField(max_length=100)
    comentario = models.CharField(max_length=100)
    ferramenta_o = models.FloatField(blank=True, null=True) #ferramenta
    ferramenta_rc = models.FloatField(blank=True, null=True) #ferramenta
    ferramenta_rib = models.FloatField(blank=True, null=True) #ferramenta
    ferramenta_alt = models.FloatField(blank=True, null=True) #ferramenta
    z_min = models.FloatField(default=0, blank=True, null=True)
    lat_2d = models.FloatField(blank=True, null=True) #sob_esp
    lat_sob_esp = models.FloatField(blank=True, null=True) #sob_esp
    vert_sob_esp = models.FloatField(blank=True, null=True) #sob_esp
    lat_passo = models.FloatField(blank=True, null=True) #passo
    vert_passo = models.FloatField(blank=True, null=True) #passo
    tol = models.FloatField(default=0, blank=True, null=True)
    rot = models.FloatField(default=0, blank=True, null=True)
    av = models.FloatField(default=0, blank=True, null=True)
    angulo = models.CharField(max_length=100)
    plano_trab = models.CharField(max_length=100)
    corte = models.CharField(max_length=100) #tempo
    total = models.CharField(max_length=100) #tempo
    fresa = models.CharField(max_length=100)
    sup = models.CharField(max_length=100)
    medicao = models.CharField(max_length=100, blank=True, null=True)
    rubrica = models.BooleanField(default=False)
    rubrica_montador = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.projeto} processo {self.programa}"