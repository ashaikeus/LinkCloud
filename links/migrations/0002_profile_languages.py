# Generated by Django 5.1.3 on 2024-12-02 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=models.ManyToManyField(related_name='profiles', to='links.language'),
        ),
    ]