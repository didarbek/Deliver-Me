# Generated by Django 4.1.1 on 2022-09-29 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_product_categories_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliverytype',
            options={'ordering': ('id',), 'verbose_name': 'Delivery Type', 'verbose_name_plural': 'Delivery Types'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('id',), 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ('id',), 'verbose_name': 'Product Category', 'verbose_name_plural': 'Product Categories'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ('id',), 'verbose_name': 'Product Image', 'verbose_name_plural': 'Product Images'},
        ),
        migrations.AlterModelOptions(
            name='productquestion',
            options={'ordering': ('id',), 'verbose_name': 'Product Question', 'verbose_name_plural': 'Product Questions'},
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ('id',), 'verbose_name': 'Product Review', 'verbose_name_plural': 'Product Reviews'},
        ),
        migrations.AlterModelOptions(
            name='productvideo',
            options={'ordering': ('id',), 'verbose_name': 'Product Video', 'verbose_name_plural': 'Product Videos'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('id',), 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterModelOptions(
            name='vote',
            options={'ordering': ('id',), 'verbose_name': 'Vote', 'verbose_name_plural': 'Votes'},
        ),
        migrations.AddField(
            model_name='vote',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
