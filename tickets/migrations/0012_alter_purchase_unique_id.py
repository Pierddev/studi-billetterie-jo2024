# Generated by Django 5.0.6 on 2024-06-28 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0011_alter_purchase_unique_id_adminlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='unique_id',
            field=models.CharField(default='649a3bb23d', max_length=10, unique=True),
        ),
    ]
