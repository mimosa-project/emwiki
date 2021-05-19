# Generated by Django 2.2.20 on 2021-05-14 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField(verbose_name='query')),
            ],
        ),
        migrations.CreateModel(
            name='Theorem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(db_index=True, max_length=30)),
                ('theorem', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HistoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relevance', models.FloatField()),
                ('click', models.BooleanField()),
                ('favorite', models.BooleanField()),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.History')),
                ('theorem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Theorem')),
            ],
        ),
    ]
