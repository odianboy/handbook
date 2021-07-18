from django_filters import rest_framework as filters
from .models import Directory, DirectoryItem


class DirectoryFilter(filters.FilterSet):
    created_date = filters.DateTimeFilter(lookup_expr='lte', field_name='version__created_date')

    class Meta:
        model = Directory
        fields = ['created_date']


class DirectoryItemFilter(filters.FilterSet):
    directory = filters.NumberFilter(field_name='directory_version__directory')
    directory_version = filters.CharFilter(field_name='directory_version__version')

    class Meta:
        model = DirectoryItem
        fields = ['directory', 'directory_version']
