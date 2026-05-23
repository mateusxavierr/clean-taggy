from django.db import models
from django.contrib.auth.models import User

class Veiculo(models.Model):
    COMBUSTIVEL_CHOICES = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL', 'Diesel'),
        ('ETANOL', 'Etanol'),
    ]
    CATEGORIA_CHOICES = [
        ('HATCH', 'Hatch Compacto (Leve)'),
        ('SEDAN', 'Sedan / SUV (Médio)'),
        ('UTILITARIO', 'Picape / Utilitário (Pesado)'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    placa = models.CharField(max_length=20, null=True, blank=True)
    tipo_combustivel = models.CharField(max_length=50, choices=COMBUSTIVEL_CHOICES)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    rendimento_exato = models.FloatField(null=True, blank=True)

    def str(self):
        return f"{self.get_categoria_display()} ({self.get_tipo_combustivel_display()})"
