# Generated by Django 4.2.6 on 2024-02-01 18:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "traffic_management",
            "0008_remove_vehicle_producer_remove_vehicle_type_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="log",
            name="Junction",
            field=models.CharField(max_length=100),
        ),
    ]
