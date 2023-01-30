# Generated by Django 4.1.5 on 2023-01-30 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Ф.И.О.')),
                ('electrical_safety_group', models.CharField(max_length=3, verbose_name='группа по электробезопасности')),
            ],
            options={
                'verbose_name': 'Работники',
                'verbose_name_plural': 'Работники',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Должность/профессия')),
            ],
            options={
                'verbose_name': 'Должность/профессия',
                'verbose_name_plural': 'Должность/профессия',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subdivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10, verbose_name='Подразделение')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
                'ordering': ['name'],
            },
        ),
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
        migrations.CreateModel(
            name='Tabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_work', models.DateField(verbose_name='Дата')),
                ('work_time', models.FloatField(blank=True, null=True, verbose_name='Время работы')),
                ('work_foreman', models.BooleanField(default=False, verbose_name='Производитель')),
                ('harmfulness', models.BooleanField(default=False, verbose_name='Вредность')),
                ('siding', models.BooleanField(default=False, verbose_name='Разъезд')),
                ('combination', models.FloatField(blank=True, null=True, verbose_name='Совмещение')),
                ('master', models.ForeignKey(limit_choices_to=models.Q(('position', 'мастер'), ('position', 'старший мастер'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master', to='tabel.person', verbose_name='Мастер')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person', to='tabel.person', verbose_name='Работник')),
                ('transferred', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transferred', to='tabel.person', verbose_name='Передан')),
                ('work_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tabel.worktype', verbose_name='Причина отсутствия')),
            ],
            options={
                'verbose_name': 'Табель рабочего времени',
                'verbose_name_plural': 'Табель рабочего времени',
                'ordering': ['date_work', 'person'],
            },
        ),
        migrations.AddField(
            model_name='person',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tabel.position', verbose_name='должность/профессия'),
        ),
        migrations.AddField(
            model_name='person',
            name='subdivision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tabel.subdivision', verbose_name='Подразделение'),
        ),
    ]
