# Generated by Django 5.1 on 2024-09-06 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botui', '0013_botcheckrun_multiproxy_botcheck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiproxy',
            name='value',
            field=models.TextField(blank=True, null=True),
        ),
    ]