# Generated by Django 4.2.1 on 2023-05-26 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TUsers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuser',
            name='modified_time',
            field=models.DateTimeField(default='05/26/2023 08:40 33 PM'),
        ),
    ]