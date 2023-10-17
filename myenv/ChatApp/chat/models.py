from datetime import datetime
from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    reply_message = models.CharField(max_length=10000000, default="Nothing to say")

class ErrorReport(models.Model):
    error_type = models.CharField(max_length=100)
    main_message = models.CharField(max_length=1000000)
    user_remarks = models.CharField(max_length=1000000)
