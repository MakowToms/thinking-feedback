# Generated by Django 4.2.3 on 2023-07-28 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('topic', '0003_grade_publish_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='your_stage',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='your_stage',
            name='user',
        ),
        migrations.AlterField(
            model_name='topic',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.stage'),
        ),
        migrations.DeleteModel(
            name='Initial_Password',
        ),
        migrations.DeleteModel(
            name='Stage',
        ),
        migrations.DeleteModel(
            name='Your_Stage',
        ),
    ]
