from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django_countries.fields import CountryField

# Create your models here.


GENDER_CHOICES = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(
        default='default_avatar.png',
        upload_to='profile_images',
        null=True,
        blank=True
    )
    date_of_birthday = models.DateField(
        null=True,
        blank=True
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=10,
        null=True,
        blank=True
    )

    phone_message = 'Phone number must be entered in the format: 01999999999'
    phone_regex = RegexValidator(
        regex=r'^(01)\d{9}$',
        message=phone_message
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=79,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
        null=True
    )
    first_name = models.CharField(
        'First Name',
        max_length=79,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        'Last Name',
        max_length=79,
        null=False,
        blank=False
    )

    phone_message = 'Phone number must be entered in the format: 01999999999'
    phone_regex = RegexValidator(
        regex=r'^(01)\d{9}$',
        message=phone_message
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=79,
        null=True,
        blank=True
    )

    address1 = models.CharField(
        'Address Line 1',
        max_length=255,
        null=False,
        blank=False
    )
    address2 = models.CharField(
        'Address Line 2',
        max_length=255,
        null=True,
        blank=True
    )
    zip_code = models.CharField(
        'ZIP',
        max_length=10,
        null=False,
        blank=False
    )
    city = models.CharField(
        'City',
        max_length=79,
        null=False,
        blank=False
    )
    country = CountryField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"
