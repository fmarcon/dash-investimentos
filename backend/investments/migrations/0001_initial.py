from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Investment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=200)),
                ("tipo", models.CharField(max_length=100)),
                ("quantidade", models.DecimalField(decimal_places=4, max_digits=16)),
                ("valor_aplicado", models.DecimalField(decimal_places=2, max_digits=18)),
                ("valor_atual_estimado", models.DecimalField(decimal_places=2, max_digits=18)),
                ("data_compra", models.DateField()),
                ("tipo_operacao", models.CharField(max_length=50)),
                ("corretora", models.CharField(blank=True, max_length=150)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="investments",
                        to="users.User",
                    ),
                ),
            ],
        ),
    ]
