from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins
from .models import UserFav
from .serializers import UserFavSerializer


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
