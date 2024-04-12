from django.db import models
from django.db.models import SlugField
from django.template.defaultfilters import slugify
from unidecode import unidecode
from PIL import Image


class Products(models.Model):
    CATEGORIES = [
        ('phones', "Phones"),
        ('laptops', "Laptops"),
        ('drones', "Drones"),
        ('cameras', "Cameras"),
        ('camera_stands', "Camera Stands"),
        ('lenses', "Lenses"),
        ('microphone', "Microphone"),
        ('other', "other"),
    ]

    device_model = models.CharField(max_length=150)
    category = models.CharField(choices=CATEGORIES, max_length=70)
    slug = SlugField(max_length=200, blank=True, null=True)
    description = models.TextField()
    rrp_price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='product_image_thumbnails', blank=True, null=True)
    release_date = models.DateField(blank=False)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product_visibility = models.BooleanField(default=False)
      
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.device_model))
        super().save(*args, **kwargs)


    def __str__(self):
        return self.device_model
