# Generated by Django 2.2.16 on 2022-09-10 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='genres',
            new_name='genre',
        ),
    ]
