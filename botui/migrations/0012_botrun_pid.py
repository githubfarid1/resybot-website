# Generated by Django 5.1 on 2024-08-21 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botui', '0011_remove_botrun_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='botrun',
            name='pid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
