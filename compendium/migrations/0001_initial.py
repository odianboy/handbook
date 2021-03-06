# Generated by Django 3.2.5 on 2021-07-18 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Наименование')),
                ('short_name', models.CharField(max_length=50, verbose_name='Короткое наименование')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.CreateModel(
            name='DirectoryVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50, verbose_name='Версия')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата начала действия справочника')),
                ('directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='version',
                                                to='compendium.directory', verbose_name='Справочник')),
            ],
            options={
                'verbose_name': 'Версия',
                'verbose_name_plural': 'Версии',
                'unique_together': {('directory', 'version')},
            },
        ),
        migrations.CreateModel(
            name='DirectoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Код элемента')),
                ('element_value', models.CharField(max_length=50, verbose_name='Значение элемента')),
                ('directory_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                        related_name='directory_item',
                                                        to='compendium.directoryversion',
                                                        verbose_name='Версия справочника')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочника',
                'unique_together': {('directory_version', 'code')},
            },
        ),
    ]
