# Generated by Django 4.1.1 on 2022-10-02 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_coupon_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/thumbnails/'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='products',
            field=models.ManyToManyField(related_name='coupon_products', to='products.product'),
        ),
    ]
