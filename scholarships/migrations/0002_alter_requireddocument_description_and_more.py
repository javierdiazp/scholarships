# Generated by Django 4.0 on 2022-01-04 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requireddocument',
            name='description',
            field=models.TextField(blank=True, max_length=300, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='description',
            field=models.TextField(blank=True, max_length=600, verbose_name='description'),
        ),
    ]
