from django.db import models

# Create your models here.
class Enterprise(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE)