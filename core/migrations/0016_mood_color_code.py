# Generated by Django 2.2.6 on 2019-12-10 21:15

import core.utils
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20191210_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='mood',
            name='color_code',
            field=core.utils.HtmlColorCodeField(default='#222222', max_length=7, validators=[core.utils.HtmlColorCodeField.is_html_color_code, core.utils.HtmlColorCodeField.is_html_color_code, core.utils.HtmlColorCodeField.is_html_color_code, core.utils.HtmlColorCodeField.is_html_color_code]),
            preserve_default=False,
        ),
    ]
