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
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-3 py-2',
            'placeholder': 'Matrícula'
        })
    )
    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-3 py-2',
            'placeholder': 'Senha'
        })
    )

    class Meta:
        model = Processo
        fields = ['medicao', 'rubrica']
        widgets = {
            'medicao': forms.TextInput(attrs={
                'class': 'form-control rounded-3 py-2',
                'placeholder': 'Medição'
            }),
            'rubrica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        if 'rubrica' in self.changed_data:
            mat = cleaned.get('matricula')
            pwd = cleaned.get('senha')
            if not mat or not pwd:
                raise ValidationError('Para alterar a rubrica, informe matrícula e senha.')
            try:
                conta = Conta.objects.get(matricula=mat)
            except Conta.DoesNotExist:
                raise ValidationError('Matrícula não encontrada.')
            user = authenticate(username=conta.user.username, password=pwd)
            if user is None:
                raise ValidationError('Senha incorreta.')
            # guardamos o user no form para usar no save()
            self._rubrica_user = user
        return cleaned

    def save(self, commit=True):
        inst = super().save(commit=False)
        # só setamos se validamos a rubrica
        if hasattr(self, '_rubrica_user'):
            inst.rubrica_user = self._rubrica_user
        if commit:
            inst.save()
        return inst


class ProcessoFerramentaEditForm(forms.ModelForm):
    matricula = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-3 py-2',
            'placeholder': 'Matrícula'
        })
    )
    senha = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-3 py-2',
            'placeholder': 'Senha'
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
        if 'rubrica_montador' in self.changed_data:
            mat = cleaned.get('matricula')
            pwd = cleaned.get('senha')
            if not mat or not pwd:
                raise ValidationError('Para alterar a rubrica de montador, informe matrícula e senha.')
            try:
                conta = Conta.objects.get(matricula=mat)
            except Conta.DoesNotExist:
                raise ValidationError('Matrícula não encontrada.')
            user = authenticate(username=conta.user.username, password=pwd)
            if user is None:
                raise ValidationError('Senha incorreta.')
            self._rm_user = user
        return cleaned

    def save(self, commit=True):
        inst = super().save(commit=False)
        if hasattr(self, '_rm_user'):
            inst.rubrica_montador_user = self._rm_user
        if commit:
            inst.save()
        return inst