# Generated by Django 4.1.5 on 2023-01-25 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_type', models.CharField(max_length=4, verbose_name='Причина отсутствия')),
            ],
            options={
                'verbose_name': 'Причина отсутствия на работе',
                'verbose_name_plural': 'Причины отсутствия на работе',
                'ordering': ['work_type'],
            },
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['name'], 'verbose_name': 'Работники', 'verbose_name_plural': 'Работники'},
        ),
        migrations.AlterField(
            model_name='person',
            name='electrical_safety_group',
            field=models.CharField(max_length=3, verbose_name='группа по электробезопасности'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Ф.И.О.'),
        ),
        migrations.AlterField(
            model_name='person',
            name='position',
            field=models.CharField(max_length=40, verbose_name='должность/профессия'),
        ),
        migrations.CreateModel(
            name='Tabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_work', models.DateField(verbose_name='Дата')),
                ('work_time', models.FloatField(verbose_name='Время работы')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tabel.person', verbose_name='Работник')),
                ('work_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tabel.worktype', verbose_name='Причина отсутствия')),
            ],
            options={
                'verbose_name': 'Табель рабочего времени',
                'verbose_name_plural': 'Табель рабочего времени',
                'ordering': ['date_work', 'person'],
            },
        ),
    ]
