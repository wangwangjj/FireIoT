from django.db import models
from django.utils import timezone
# Create your models here.

class Data(models.Model):
    huilu = models.CharField(max_length=200)
    addr = models.CharField(max_length=200)
    item = models.TextField()
    state = models.TextField()
    pub_date = models.CharField(max_length=200)

    class Meta:
        db_table = 'Data'

    def __unicode__(self):
        return self

class Data1(models.Model):
    state = models.TextField()
    pub_date = models.CharField(max_length=200)

    class Meta:
        db_table = 'Data1'

    def __unicode__(self):
        return self
