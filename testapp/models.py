from django.contrib.auth.models import User
from .models import *
from django.utils import timezone
from django.db import models

# Create your models here.




class testmodel(models.Model):
    fk = models.IntegerField(blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'testtable'
