# Generated by Django 3.2.15 on 2022-12-07 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explanation', '0004_auto_20221206_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanation',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
