# Generated by Django 4.2.6 on 2024-02-03 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("traffic_management", "0010_delete_fine"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fine", models.IntegerField()),
                ("status", models.CharField(max_length=10)),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="traffic_management.owner",
                    ),
                ),
            ],
        ),
    ]
