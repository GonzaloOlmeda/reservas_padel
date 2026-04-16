from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    telefono = forms.CharField(max_length=15, required=False, label="Teléfono (opcional)")

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.telefono = self.cleaned_data.get('telefono', '')
        user.rol = 'usuario'
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label