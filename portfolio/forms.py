from django import forms
from .models import Programa, Asignatura

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del programa'}),
        }

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'programa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la asignatura'}),
            'programa': forms.Select(attrs={'class': 'form-select'}),
        }