from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Veiculo(models.Model):
    # Opções fixas para evitar erros de digitação no banco e quebrar o cálculo
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

    marca = models.CharField(max_length=100, null=True, blank=True)
    ano = models.IntegerField(null=True, blank=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    placa = models.CharField(max_length=20, null=True, blank=True)
    
    tipo_combustivel = models.CharField(max_length=50, choices=COMBUSTIVEL_CHOICES)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, null=True, blank=True)
    rendimento_exato = models.FloatField(null=True, blank=True)


    def __str__(self):
        return f"{self.get_categoria_display()} ({self.get_tipo_combustivel_display()})"


class Transacao(models.Model):
    STATUS_CHOICES = [
        ('FATURADA', 'Faturada'),
        ('PENDENTE', 'Pendente'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    local = models.CharField(max_length=255)
    valor_pedagio = models.DecimalField(max_digits=10, decimal_places=2)
    co2_economizado = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    fator_co2 = models.FloatField(null=True, blank=True)
    km_estimado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.local} - {self.data}"


class RegistroEmissao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    distancia_percorrida = models.FloatField()
    co2_emitido_kg = models.FloatField()
    usou_fallback = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)

class MetaSustentabilidade(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.CharField(max_length=50, default='target')
    objetivo_kg = models.FloatField(help_text="Quantos kg de CO2 economizar para bater a meta")

    def __str__(self):
        return self.titulo

class MetaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    meta = models.ForeignKey(MetaSustentabilidade, on_delete=models.CASCADE)
    progresso_kg = models.FloatField(default=0.0)
    concluida = models.BooleanField(default=False)
    data_adicao = models.DateTimeField(auto_now_add=True)

    def percentual(self):
        if self.meta.objetivo_kg == 0: return 100
        p = (self.progresso_kg / self.meta.objetivo_kg) * 100
        return min(100, int(p))      

    def __str__(self):
        return f"{self.usuario.username} - {self.meta.titulo}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    estado = models.CharField(max_length=100, null=True, blank=True, help_text="Estado onde o usuário reside, para cálculo de ICMS")
    cidade = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    