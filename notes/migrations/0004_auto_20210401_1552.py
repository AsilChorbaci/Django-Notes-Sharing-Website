# Generated by Django 3.1.7 on 2021-04-01 12:52

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]