# Generated by Django 2.2.16 on 2022-09-10 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Рейтинг'),
        ),
    ]
