# Generated by Django 2.2.3 on 2019-08-15 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inputtools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordlist',
            name='word',
            field=models.TextField(db_index=True, max_length=255, unique=True),
        ),
    ]
