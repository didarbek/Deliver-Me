# Generated by Django 4.1.1 on 2022-09-29 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_deliverytype_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_votes', to='products.productquestion'),
        ),
    ]
