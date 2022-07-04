# Generated by Django 4.0.6 on 2022-07-04 08:12

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('myblog', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
