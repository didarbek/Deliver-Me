from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

MEMBERSHIP_CHOICES = (
    ('Premium', 'premium'),
    ('Free', 'free')
)


class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=15
    )
    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10
    )

    def __str__(self):
        return self.membership_type

    def save(self, *args, **kwargs):
        """
        Saving our membership with adding a slug
        @param args:
        @param kwargs:
        @return:
        """
        if not self.slug:
            self.slug = slugify(self.membership_type)
        return super().save(*args, **kwargs)


class UserMembership(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user_membership',
        on_delete=models.CASCADE
    )
    membership = models.ForeignKey(
        Membership,
        related_name='user_membership',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership,
        related_name='subscription',
        on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

