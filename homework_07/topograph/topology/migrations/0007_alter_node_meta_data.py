# Generated by Django 4.0.3 on 2022-04-12 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topology', '0006_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='meta_data',
            field=models.JSONField(default=dict),
        ),
    ]
