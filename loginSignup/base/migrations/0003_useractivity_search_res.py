# Generated by Django 5.0.1 on 2024-02-02 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_useractivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='search_res',
            field=models.TextField(default=255),
            preserve_default=False,
        ),
    ]
