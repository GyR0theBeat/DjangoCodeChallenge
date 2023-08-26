from rest_framework import serializers
from .models import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PlaceSearchSerializer(serializers.Serializer):
    query = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    distance = serializers.FloatField() 