# Generated by Django 2.2.3 on 2019-08-02 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wordlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField(db_index=True, unique=True)),
                ('lang', models.CharField(choices=[('EN', 'English'), ('HI', 'Hindi')], default='EN', max_length=2)),
            ],
        ),
    ]
