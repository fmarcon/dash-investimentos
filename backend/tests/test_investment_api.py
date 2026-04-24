from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from investments.models import Investment
from users.models import User


class InvestmentApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="buyer@example.com", password="secure1234")
        login_url = reverse("login")
        response = self.client.post(login_url, {"email": "buyer@example.com", "password": "secure1234"}, format="json")
        self.access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_create_investment_and_list(self):
        url = reverse("investment-list")
        payload = {
            "nome": "Ação Azul",
            "tipo": "Ação",
            "quantidade": "15.00",
            "valor_aplicado": "1500.00",
            "valor_atual_estimado": "1800.00",
            "data_compra": "2026-04-01",
            "tipo_operacao": "compra",
            "corretora": "InvestPro",
        }
        create_response = self.client.post(url, payload, format="json")
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["lucro_prejuizo"], Decimal("300.00"))

        list_response = self.client.get(url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["nome"], "Ação Azul")

    def test_update_and_delete_investment(self):
        investment = Investment.objects.create(
            user=self.user,
            nome="FII Varejo",
            tipo="FII",
            quantidade="10.00",
            valor_aplicado="1000.00",
            valor_atual_estimado="1100.00",
            data_compra="2026-03-01",
            tipo_operacao="compra",
            corretora="MercadoInvest",
        )
        detail_url = reverse("investment-detail", args=[investment.id])
        update_payload = {"valor_atual_estimado": "1200.00"}
        update_response = self.client.patch(detail_url, update_payload, format="json")
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["lucro_prejuizo"], Decimal("200.00"))

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Investment.objects.filter(id=investment.id).exists())
