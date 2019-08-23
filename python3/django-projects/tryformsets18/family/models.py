from django.db import models

# Create your models here.

class FamilyMember(models.Model):
    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField(null=True, blank=True)
    job = models.CharField(max_length=20, null=True, blank=True)
    parent = models.ForeignKey('self',
                               blank=True,
                               null=True,
                               related_name='children',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name
