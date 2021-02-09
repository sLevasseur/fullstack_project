from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class databaseForBlogs(models.Model):
    title = models.CharField(max_length=100)
    text = HTMLField()
    img_height = models.PositiveBigIntegerField(null=True, blank=True)
    img_width = models.PositiveBigIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="images_for_blogs/",
                              null=True, blank=True)
    # "image" variable is not used on the front part. It's because the hosting provider I
    # used (heroku) don't actually allow to host images without deleting them :/
    # I left it here while i found a solution, I heard about AWS S3, i will check it.
    date = models.DateTimeField(auto_now_add=True)


class databaseForNewsletter(models.Model):
    email = models.EmailField(default="test@gmail.com")


class databaseForCoordinates(models.Model):
    url_coordinates = models.CharField(max_length=500) # in the admin view copy paste a google map url
    name_of_locations = models.CharField(max_length=300)
    adresse = models.CharField(max_length=300)
    code_postal = models.CharField(max_length=300)
    localite = models.CharField(max_length=300)
    informations_supplementaires = HTMLField()

    # url_coordinates = url of a google map location
    # the algorithm (serializer.py) is base on google map to find the exact gps coordinates
