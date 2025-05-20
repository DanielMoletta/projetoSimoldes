from django.db import models

from django.db import models

class Aperto(models.Model):
    class Meta:
        verbose_name = 'Aperto'
        verbose_name_plural = 'Apertos'

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Tipo_Percurso(models.Model):
    class Meta:
        verbose_name = 'Tipo de Percurso'
        verbose_name_plural = 'Tipos de Percurso'

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Referencia(models.Model):
    class Meta:
        verbose_name = 'Referência'	
        verbose_name_plural = 'Referências'

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Angulo(models.Model):
    class Meta:
        verbose_name = 'Ângulo'
        verbose_name_plural = 'Ângulos'

    nome = models.ForeignKey(Aperto, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome}"
    
class Plano_Trabalho(models.Model):
    class Meta:
        verbose_name = 'Plano de Trabalho'	
        verbose_name_plural = 'Planos de Trabalho'

    nome = models.ForeignKey(Aperto, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome}"

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
    aperto = models.ForeignKey(Aperto, on_delete=models.PROTECT)
    tempo_projeto = models.CharField(max_length=100)
    centro_bloco = models.CharField(max_length=100)
    referencia_z = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='media/', blank=True, null=True)
    observacao = models.CharField(max_length=100)

    def __str__(self):
        return f"Programa - {self.id}"

class Processo(models.Model):
    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
     
    projeto = models.ForeignKey(Projeto, on_delete=models.PROTECT)
    setup_inicio = models.DateField(auto_now=False, auto_now_add=False)
    setup_hora_ini = models.CharField(max_length=100)
    setup_termino = models.DateField(auto_now=False, auto_now_add=False)
    setup_hora_ter = models.CharField(max_length=100)
    usina_inicio = models.DateField(auto_now=False, auto_now_add=False)
    usina_hora_ini = models.CharField(max_length=100)
    usina_termino = models.DateField(auto_now=False, auto_now_add=False)
    usina_hora_ter = models.CharField(max_length=100)
    programa = models.AutoField(primary_key=True)
    tipo_percurso = models.ForeignKey(Tipo_Percurso, on_delete=models.PROTECT)
    referencia = models.ForeignKey(Referencia, on_delete=models.PROTECT)
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
    angulo = models.ForeignKey(Angulo, on_delete=models.PROTECT)
    plano_trab = models.ForeignKey(Plano_Trabalho, on_delete=models.PROTECT)
    corte = models.CharField(max_length=100) #tempo
    total = models.CharField(max_length=100) #tempo
    fresa = models.CharField(max_length=100)
    sup = models.CharField(max_length=100)
    medicao = models.CharField(max_length=100)
    rubrica = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.projeto} processo {self.programa}"