import uuid
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


CONDITION_CHOICES = (
    ("NEW", "New"),
    ("USED", "Used"),
    ("OPEN_BOX", "Open Box"),
    ("REFURBISHED", "Refurbished"),
)

RATING_CHOICES = (
    ('1', 'Avoid'),
    ('2', 'Sub Par'),
    ('3', 'Okay'),
    ('4', 'Good'),
    ('5', 'Outstanding')
)

VOTE_CHOICES = (
    ("LIKE", "Like"),
    ("DISLIKE", "Dislike")
)


class Tag(models.Model):
    title = models.CharField(max_length=79)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('id',)


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to='product_images',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    thumbnail = models.ImageField(
        upload_to='product_images/thumbnails/',
        null=True,
        blank=True
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images',
        null=True,
        blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.product.title}'

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ('id',)

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)

    def make_thumbnail(self, image, size=(300, 200)):
        """
        Method to create a square thumbnail of image
        @param image:
        @param size:
        @return:
        """
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class ProductVideo(models.Model):
    video = models.FileField(
        upload_to='product_videos',
        validators=[FileExtensionValidator(['mp4', 'mov', 'flv', 'mkv', 'avi'])]
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='videos',
        null=True,
        blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.product.title}'

    class Meta:
        verbose_name = 'Product Video'
        verbose_name_plural = 'Product Videos'
        ordering = ('id',)


class ProductCategory(models.Model):
    title = models.CharField(max_length=79, null=False, blank=False)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ('id',)


class DeliveryType(models.Model):
    type = models.CharField(max_length=79, null=False, blank=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False
    )
    estimated_time = models.CharField(max_length=79, null=False, blank=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.type} - {self.price}'

    class Meta:
        verbose_name = 'Delivery Type'
        verbose_name_plural = 'Delivery Types'
        ordering = ('id',)


class ProductQuestion(models.Model):
    text = models.TextField(null=False, blank=False)
    votes = models.IntegerField(default=0)
    likes = models.ManyToManyField(
        User,
        related_name='question_likes',
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='question_dislikes',
        blank=True
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.SET_NULL
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.text} - {self.user}'

    class Meta:
        verbose_name = 'Product Question'
        verbose_name_plural = 'Product Questions'
        ordering = ('id',)


class ProductReview(models.Model):
    title = models.CharField(max_length=79, null=False, blank=False)
    description = models.TextField(null=False)
    rating = models.CharField(
        choices=RATING_CHOICES,
        max_length=15,
        null=False,
        blank=False
    )
    found_helpful = models.ManyToManyField(
        User,
        related_name='found_review_helpful',
        blank=True
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.title}'

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ('id',)

    @property
    def get_author(self):
        return self.author.email


class Coupon(models.Model):
    seller = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='coupon_owner',
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        User,
        'coupon_users',
        blank=True
    )
    products = models.ManyToManyField(
        'Product',
        related_name='coupon_products'
    )
    code = models.CharField(
        max_length=79,
        unique=True
    )
    valid_from = models.DateTimeField(null=True)
    valid_to = models.DateTimeField(null=True)
    discount_amount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    coupons_amount = models.PositiveIntegerField(null=False, blank=False)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ('id',)

    @classmethod
    def generate_code(cls):
        return uuid.uuid4().hex


class Product(models.Model):
    title = models.CharField(max_length=79, null=False, blank=False)
    slug = models.SlugField(max_length=79, null=True, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False
    )
    discount = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    condition = models.CharField(
        choices=CONDITION_CHOICES,
        max_length=15,
        null=False,
        blank=False
    )
    category = models.ForeignKey(
        'ProductCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    delivery_type = models.ForeignKey(
        'DeliveryType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField('Tag')

    is_active = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.title} - {self.seller}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('id',)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """
        Saving our product with adding a slug
        @param args:
        @param kwargs:
        @return:
        """
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_rating(self):
        """
        Method to get the rating of particular product
        @return:
        """
        total = 0
        if self.reviews.all():
            for s in self.reviews.all():
                for review in s.rating:
                    total += int(review)
            return total
        else:
            return 0


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    wished_products = models.ManyToManyField(Product)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
        ordering = ('id',)


class BrowsingHistory(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Browsing History'
        verbose_name_plural = 'Browsing Histories'
        ordering = ('id',)
