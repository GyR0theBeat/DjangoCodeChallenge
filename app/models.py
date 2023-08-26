"""
Definition of models.
"""

from django.contrib.gis.db import models
from django.contrib.postgres.fields import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.PointField()
    search_vector = SearchVectorField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Meta:
        indexes = [GinIndex(fields=['search_vector'])]
