# Generated by Django 2.2 on 2021-02-22 16:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0003_auto_20210222_1601'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Posts',
        ),
    ]
