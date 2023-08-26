from django.db import models
from django.contrib.auth.models import User


class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    area = models.FloatField(null=True, blank=True)  # Added field for area
    volume = models.FloatField(null=True, blank=True)  # Added field for volume

    # ... other fields and methods ...

    def save(self, *args, **kwargs):
        self.area = self.length * self.breadth if self.length and self.breadth else None
        self.volume = self.length * self.breadth * \
            self.height if self.length and self.breadth and self.height else None
        super().save(*args, **kwargs)
