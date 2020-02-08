# Generated by Django 2.2.6 on 2020-02-08 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_userprofile_read_encouraging_sentences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='agency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Agency'),
            preserve_default=False,
        ),
    ]
