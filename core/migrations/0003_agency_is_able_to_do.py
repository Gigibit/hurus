# Generated by Django 2.2.7 on 2019-11-07 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191107_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='is_able_to_do',
            field=models.BooleanField(default=False),
        ),
    ]
