# Generated by Django 4.1.1 on 2022-09-30 18:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0013_delete_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='found_helpful',
            field=models.ManyToManyField(blank=True, related_name='found_review_helpful', to=settings.AUTH_USER_MODEL),
        ),
    ]