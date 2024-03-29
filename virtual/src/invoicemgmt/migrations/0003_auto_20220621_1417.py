# Generated by Django 3.2.7 on 2022-06-21 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicemgmt', '0002_payments_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payee', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Mlipwaji')),
                ('description', models.TextField(blank=True, default='', max_length=20, null=True, verbose_name='Maelezo ya malipo')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Kiasi cha malipo')),
                ('proof_of_payment', models.FileField(default='default.png', upload_to='Proofs_expenses')),
                ('updated_by', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Paid By')),
            ],
        ),
        migrations.RemoveField(
            model_name='payments',
            name='payment_type',
        ),
    ]
