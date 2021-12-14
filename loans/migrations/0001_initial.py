# Generated by Django 4.0 on 2021-12-14 15:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='amount')),
                ('term', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='term in years')),
                ('down_payment', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='down payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='accounts.user', verbose_name='user')),
            ],
            options={
                'verbose_name': 'loan',
                'verbose_name_plural': 'loans',
            },
        ),
    ]