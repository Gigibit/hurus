# Generated by Django 2.2.6 on 2020-02-08 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200208_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='course_to_see',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Course'),
        ),
    ]