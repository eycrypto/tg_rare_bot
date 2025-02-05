# Generated by Django 4.2.7 on 2023-12-09 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='system',
            name='cooldown',
        ),
        migrations.AddField(
            model_name='system',
            name='max',
            field=models.PositiveIntegerField(default=150, verbose_name='Максимальная частота отправки сообщений'),
        ),
        migrations.AddField(
            model_name='system',
            name='min',
            field=models.PositiveIntegerField(default=50, verbose_name='Минимальная частота отправки сообщений'),
        ),
        migrations.CreateModel(
            name='SendMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='Время отправки сообщения')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Models.message', verbose_name='Отправленое сообщение')),
            ],
        ),
    ]
