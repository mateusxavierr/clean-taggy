from django import forms
from .models import veiculo

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['tipo_combustivel', 'categoria', 'rendimento_exato']

        labels = {
            'tipo_combustivel': 'Tipo de Combustível',
            'categoria': 'Categoria do Veículo',
            'rendimento_exato': 'Rendimento Exato (km/l) - Opcional',
        }

        widgets = {
            'rendimento_exato': forms.NumberInput(attrs={
                'placeholder': '0.01',
                'step': '0.01'
            }),
        }