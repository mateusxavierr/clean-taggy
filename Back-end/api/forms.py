from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistroClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirme a Senha")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {
            'username': 'Nome de Usuário',
            'first_name': 'Nome Completo',
            'email': 'E-mail'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes do Tailwind a todos os inputs gerados pelo Django
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-green-500',
                'required': 'required'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso. Faça login ou tente outro.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")

        if password:
            if len(password) < 8:
                self.add_error('password', "A senha deve ter pelo menos 8 caracteres.")
            if not re.search(r'[A-Za-z]', password):
                self.add_error('password', "A senha deve conter pelo menos uma letra.")
            if not re.search(r'[0-9]', password):
                self.add_error('password', "A senha deve conter pelo menos um número.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Criptografa a senha antes de salvar no banco de dados (Padrão Django)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user