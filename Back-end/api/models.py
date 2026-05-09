from django.db import models

class Transacao(models.Model):
    local = models.CharField(max_length=255)
    valor_pedagio = models.DecimalField(max_digits=10, decimal_places=2)
    co2_economizado = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.local} - {self.data}"


