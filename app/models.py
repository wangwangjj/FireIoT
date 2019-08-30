from django.db import models
from django.utils import timezone
# Create your models here.

class Data(models.Model):
    huilu = models.CharField(max_length=200)
    addr = models.CharField(max_length=200)
    item = models.TextField()
    state = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-pub_date',)
        db_table = 'FireData'

    def __unicode__(self):
        return self
