# Generated by Django 4.1.1 on 2022-09-29 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productquestion',
            old_name='answer',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='productquestion',
            name='question',
        ),
    ]
