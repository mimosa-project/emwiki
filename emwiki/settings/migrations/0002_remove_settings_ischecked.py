# Generated by Django 3.2.25 on 2024-05-11 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='isChecked',
        ),
    ]
