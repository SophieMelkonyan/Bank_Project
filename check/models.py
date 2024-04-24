from django.utils import timezone
from django.db import models


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, default="")
    created_at = models.DateTimeField(default=timezone.now)
    number = models.IntegerField(default=0)
    windows = models.IntegerField(default=0)
    number1_available = models.BooleanField(default=True)
    number2_available = models.BooleanField(default=True)

