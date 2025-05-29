from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Projeto
from .models import Processo
from contas.models import Conta

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg fs-4 rounded-3 shadow-sm',
            'placeholder': 'Digite seu email',
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg fs-4 rounded-3 shadow-sm',
            'placeholder': 'Digite sua senha',
        })
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não correspondem")

        return cleaned_data

class ProjetoEditForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = [
            'setup_inicio', 'setup_hora_ini', 'setup_termino', 'setup_hora_ter',
            'usina_inicio', 'usina_hora_ini', 'usina_termino', 'usina_hora_ter'
        ]
        widgets = {
            'setup_inicio': forms.DateInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'date'
            }),
            'setup_hora_ini': forms.TimeInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'time'
            }),
            'setup_termino': forms.DateInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'date'
            }),
            'setup_hora_ter': forms.TimeInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'time'
            }),
            'usina_inicio': forms.DateInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'date'
            }),
            'usina_hora_ini': forms.TimeInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'time'
            }),
            'usina_termino': forms.DateInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'date'
            }),
            'usina_hora_ter': forms.TimeInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'dd/mm/aaaa',
                'type': 'time'
            }),
        }

class ProcessoEditForm(forms.ModelForm):
    matricula = forms.CharField(
        label='Matrícula',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua matrícula'
        })
    )
    senha = forms.CharField(
        label='Senha',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

    class Meta:
        model = Processo
        fields = ['medicao', 'rubrica']
        widgets = {
            'medicao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a medição'
            }),
            'rubrica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        rubrica = cleaned.get('rubrica')
        matricula = cleaned.get('matricula')
        senha = cleaned.get('senha')

        # Se for tentar marcar/desmarcar a rubrica, exige credenciais válidas
        # (comparar com o app 'contas', campo Conta.matricula)
        if 'rubrica' in self.changed_data:
            # Então o usuário alterou rubrica: exige matrícula e senha
            if not matricula or not senha:
                raise ValidationError('Para alterar a rubrica, informe matrícula e senha.')
            try:
                conta = Conta.objects.get(matricula=matricula)
            except Conta.DoesNotExist:
                raise ValidationError('Matrícula não encontrada.')
            user = authenticate(username=conta.user.username, password=senha)
            if user is None:
                raise ValidationError('Senha incorreta para a matrícula informada.')

        return cleaned

class ProcessoFerramentaEditForm(forms.ModelForm):
    matricula = forms.CharField(
        label='Matrícula',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua matrícula'
        })
    )
    senha = forms.CharField(
        label='Senha',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )

    class Meta:
        model = Processo
        fields = ['rubrica_montador']
        widgets = {
            'rubrica_montador': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        # Se o usuário mudou o valor de rubrica_montador, exige credenciais válidas
        if 'rubrica_montador' in self.changed_data:
            matricula = cleaned.get('matricula')
            senha = cleaned.get('senha')

            if not matricula or not senha:
                raise ValidationError('Para alterar a rubrica do montador, informe matrícula e senha.')

            # busca a Conta pela matrícula
            try:
                conta = Conta.objects.get(matricula=matricula)
            except Conta.DoesNotExist:
                raise ValidationError('Matrícula não encontrada.')

            # autentica pelo User associado
            user = authenticate(username=conta.user.username, password=senha)
            if user is None:
                raise ValidationError('Senha incorreta para a matrícula informada.')

        return cleaned