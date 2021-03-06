# Generated by Django 3.2.9 on 2021-11-19 11:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0005_rename_author_staff_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='姓')),
                ('tel', models.CharField(blank=True, max_length=100, null=True, verbose_name='電話番号')),
                ('remarks', models.CharField(blank=True, max_length=100, verbose_name='備考')),
                ('start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='開始時間')),
                ('end', models.DateTimeField(default=django.utils.timezone.now, verbose_name='終了時間')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.staff', verbose_name='スタッフ')),
            ],
        ),
    ]
