from django.conf import settings
from django.db import models


class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="investments")
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=16, decimal_places=4)
    valor_aplicado = models.DecimalField(max_digits=18, decimal_places=2)
    valor_atual_estimado = models.DecimalField(max_digits=18, decimal_places=2)
    data_compra = models.DateField()
    tipo_operacao = models.CharField(max_length=50)
    corretora = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def lucro_prejuizo(self):
        return self.valor_atual_estimado - self.valor_aplicado

    def __str__(self):
        return f"{self.nome} - {self.user.email}"
