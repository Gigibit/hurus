# Generated by Django 2.2.7 on 2019-11-07 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncouragingSentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('language', models.CharField(choices=[('DE', 'German'), ('IT', 'Italian'), ('EN', 'English')], default='DE', max_length=2)),
            ],
        ),
        migrations.RemoveField(
            model_name='agency',
            name='manager',
        ),
        migrations.AddField(
            model_name='employee',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='agency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Agency'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(choices=[('DE', 'German'), ('IT', 'Italian'), ('EN', 'English')], default='DE', max_length=2),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='read_encouraging_sentences',
            field=models.ManyToManyField(to='core.EncouragingSentence'),
        ),
    ]
