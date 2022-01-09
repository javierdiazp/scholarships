# Generated by Django 4.0 on 2022-01-04 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_first_name_alter_user_last_name'),
        ('scholarships', '0001_initial'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_documents', to='accounts.user', verbose_name='reviewed by'),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='accounts.user', verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='rooms.room', verbose_name='room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='scholarship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='scholarships.scholarship', verbose_name='scholarship'),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_logs', to='rooms.room', verbose_name='room'),
        ),
    ]