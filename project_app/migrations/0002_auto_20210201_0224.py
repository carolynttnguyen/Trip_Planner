# Generated by Django 2.2 on 2021-02-01 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='planned_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='project_app.User'),
        ),
    ]
