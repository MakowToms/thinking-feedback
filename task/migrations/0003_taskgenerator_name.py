# Generated by Django 4.2.3 on 2023-11-12 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskgenerator',
            name='name',
            field=models.CharField(default='generator', max_length=40),
            preserve_default=False,
        ),
    ]
