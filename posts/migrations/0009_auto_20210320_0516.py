# Generated by Django 2.2.6 on 2021-03-20 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20210320_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Идентификатор_группы'),
        ),
    ]
