# Generated by Django 4.2.7 on 2023-11-06 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='importat',
            new_name='important',
        ),
    ]