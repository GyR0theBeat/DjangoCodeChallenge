"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

from rest_framework import generics
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializer

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import generics
from django.contrib.gis.db.models.functions import Distance as DistanceFunc
from .models import Place
from .serializers import PlaceSearchSerializer, PlaceSerializer
from django.db.models import F

class PlaceListCreateView(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class PlaceDeleteView(generics.DestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


class PlaceSearchView(generics.ListAPIView):
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'description']  # Filter by name and description

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        latitude = self.request.query_params.get('latitude', 0)
        longitude = self.request.query_params.get('longitude', 0)
        distance = self.request.query_params.get('distance', 0)

        user_location = Point(float(longitude), float(latitude), srid=4326)
        queryset = Place.objects.annotate(
            search=SearchRank(F('search_vector'), SearchQuery(query)),
            distance=DistanceFunc('location', user_location)
        ).filter(search__gt=0).order_by('-search', 'distance')

        if distance:
            queryset = queryset.filter(location__distance_lte=(user_location, Distance(km=distance)))

        return queryset