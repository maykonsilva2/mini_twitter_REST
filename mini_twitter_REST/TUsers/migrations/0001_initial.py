# Generated by Django 4.2.1 on 2023-05-26 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('modified_time', models.DateTimeField(default='05/26/2023 03:57 33 AM')),
                ('token', models.CharField(max_length=10000, null=True)),
            ],
        ),
    ]
