# Generated by Django 4.1.1 on 2022-10-29 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_productimage_thumbnail_alter_coupon_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.productcategory'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.CharField(choices=[('1', 'Avoid'), ('2', 'Sub Par'), ('3', 'Okay'), ('4', 'Good'), ('5', 'Outstanding')], max_length=15),
        ),
    ]
