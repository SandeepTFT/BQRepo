from django.db import models

# Create your models here.
class TableA(models.Model):

    visitID = models.CharField(max_length=50)
    Date = models.IntegerField()

    def __str__(self):
        return self.visitID

    class meta():
        
        