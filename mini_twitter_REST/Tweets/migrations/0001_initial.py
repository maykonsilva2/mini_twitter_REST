# Generated by Django 4.2.1 on 2023-05-26 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TUsers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TCtweets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_text', models.CharField(max_length=280, null=True)),
                ('time', models.DateTimeField(default='05/26/2023 03:57 33 AM')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TUsers.tuser')),
            ],
        ),
    ]
