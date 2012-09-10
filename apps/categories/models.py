from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=75)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
