# Generated by Django 2.2.3 on 2020-09-21 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0007_remove_post_excerpt'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, max_length=400, verbose_name='摘要'),
        ),
    ]
