from rest_framework import serializers
from .models import Investment


class InvestmentSerializer(serializers.ModelSerializer):
    lucro_prejuizo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Investment
        fields = [
            "id",
            "nome",
            "tipo",
            "quantidade",
            "valor_aplicado",
            "valor_atual_estimado",
            "data_compra",
            "tipo_operacao",
            "corretora",
            "lucro_prejuizo",
        ]

    def get_lucro_prejuizo(self, obj):
        return obj.lucro_prejuizo
