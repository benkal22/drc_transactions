# Generated by Django 5.0.6 on 2024-07-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='transaction',
            name='amount_with_tva',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='transaction',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/transactions/'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='tva_rate',
            field=models.DecimalField(decimal_places=2, default=0.16, max_digits=5),
        ),
        migrations.AlterField(
            model_name='client',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/clients/'),
        ),
        migrations.AlterField(
            model_name='producer',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/producers/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/products/'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/suppliers/'),
        ),
        migrations.AlterField(
            model_name='uniquesector',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/uniquesectors/'),
        ),
    ]