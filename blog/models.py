from django.db import models
from datetime import date

class Blog(models.Model):
    name        = models.CharField(max_length=20, blank=False)
    email       = models.CharField(max_length=30)
    subject     = models.CharField(max_length=20, blank=False)
    date        = models.DateField(default=date.today)
    description = models.TextField(null=False, blank=False)
    

    def __str__(self):
        return self.name