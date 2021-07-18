from django.db.models import Prefetch, Max

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend

from .models import Directory, DirectoryItem, DirectoryVersion
from .serializers import (
    DirectoryListSerializer,
    DirectoryDetailSerializer,
    DirectoryItemListSerializer
)
from .filters import DirectoryFilter, DirectoryItemFilter


class DirectoryListView(generics.GenericAPIView):
    """
    Получение списка справочников.
    """
    serializer_class = DirectoryListSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = DirectoryFilter
    queryset = Directory.objects.all().distinct()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self.setup_eager_loading(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def setup_eager_loading(self, queryset):
        latest_versions = DirectoryVersion.objects.values_list(
            'directory'
        ).annotate(max_id=Max('id')).values_list('max_id', flat=True)

        return queryset.prefetch_related(
            'version',
            'version__directory_item',
            Prefetch(
                'version',
                queryset=DirectoryVersion.objects.filter(pk__in=latest_versions),
                to_attr='current_version'
            ),
            'current_version__directory_item'
        )


class DirectoryItemListView(generics.GenericAPIView):
    """
    Получение списка элементов справочников
    """
    serializer_class = DirectoryItemListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = DirectoryItemFilter
    queryset = DirectoryItem.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.select_related('directory_version')

        # Валидация элементов заданного справочника текущей версии.
        if 'directory' in request.GET:
            pk = request.GET['directory']
            directories = Directory.objects.all()
            if not directories.filter(pk=pk).exists():
                directory_id = [directory.id for directory in directories]
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data=f'Справочник со значением {pk} отсутствует. Список имеющихся справочников:'
                                     f' {directory_id}')

        # Валидация элементов заданного справочника по указанной версии.
        if 'directory_version' in request.GET:
            version = request.GET['directory_version']
            versions = DirectoryVersion.objects.all()
            if not versions.filter(version=version).exists():
                version_value = [ver.version for ver in versions]

                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data=f'Версия со значением {version} отсутствует. Список имеющихся версий:'
                                     f' {version_value}')

        # Получение элементов заданного справочника текущей версии.
        if 'directory_version' not in request.GET:
            latest_versions = DirectoryVersion.objects.values_list(
                'directory'
            ).annotate(max_id=Max('id')).values_list('max_id', flat=True)
            queryset = queryset.filter(directory_version__in=latest_versions)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DirectoryDetailView(APIView):
    """
    Получение указанного справочника.
    """
    def get(self, request, pk):
        directory = Directory.objects.get(id=pk)
        serializer = DirectoryDetailSerializer(directory)
        return Response(serializer.data)
