import django_filters
from .models import WasteSite , Video
from django import forms

class WasteSiteFilter(django_filters.FilterSet):
    city_name = django_filters.CharFilter(field_name='city_name', lookup_expr='icontains')
    class Meta:
        model = WasteSite
        fields = ['city_name',]