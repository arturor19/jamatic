# Generated by Django 5.0.2 on 2024-09-01 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linerCRM', '0003_instalaciondeservicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='instalaciondeservicio',
            name='servicio_completado',
            field=models.BooleanField(default=False),
        ),
    ]
