from django.db import models


class Maintenance(models.Model):
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    machine = models.CharField(max_length=255)
    proplem = models.TextField()
    tel = models.CharField(max_length=12)

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
