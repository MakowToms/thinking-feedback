# Generated by Django 4.2.3 on 2023-09-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('tick', '✓'), ('cross', '☓'), ('G', 'G'), ('B', 'B'), ('nb', 'nb')], default='nb', max_length=5)),
                ('type', models.CharField(choices=[('T', 'Test'), ('C', 'Conversation'), ('O', 'Observation')], default=1, max_length=1)),
                ('comment', models.CharField(max_length=200)),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
