# Generated by Django 3.2.9 on 2021-11-12 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='portfolio.category', verbose_name='カテゴリ'),
            preserve_default=False,
        ),
    ]