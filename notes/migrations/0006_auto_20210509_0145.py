# Generated by Django 3.1.7 on 2021-05-08 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_auto_20210509_0049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='Parent',
            new_name='parent',
        ),
    ]
