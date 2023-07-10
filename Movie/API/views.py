from django.shortcuts import render
from rest_framework import generics
from .serializers import MovieSerializer
from .models import Movie

class MovieCreateList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Create your views here.
