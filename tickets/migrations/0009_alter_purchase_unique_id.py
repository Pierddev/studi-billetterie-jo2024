# Generated by Django 5.0.6 on 2024-06-26 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_alter_purchase_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='unique_id',
            field=models.CharField(default='a8de8ee745', max_length=10, unique=True),
        ),
    ]
