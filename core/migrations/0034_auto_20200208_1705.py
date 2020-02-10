# Generated by Django 2.2.6 on 2020-02-08 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_userprofile_seen_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='core.Team'),
        ),
        migrations.AlterField(
            model_name='tought',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toughts', to='core.Employee'),
        ),
        migrations.AlterField(
            model_name='tought',
            name='mood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Mood'),
        ),
    ]
