from rest_framework import serializers

from .models import Directory, DirectoryItem, DirectoryVersion


class DirectoryItemListSerializer(serializers.ModelSerializer):
    """
    Элементы справочника.
    """
    version = serializers.SerializerMethodField()

    class Meta:
        model = DirectoryItem
        fields = ('version', 'code', 'element_value')

    def get_version(self, item):
        return item.directory_version.version


class DirectoryVersionSerializer(serializers.ModelSerializer):
    """
    Список версий.
    """
    directory_item = DirectoryItemListSerializer(many=True)

    class Meta:
        model = DirectoryVersion
        fields = ('id', 'directory', 'version', 'created_date', 'directory_item')


class DirectoryListSerializer(serializers.ModelSerializer):
    """
    Список справочников.
    """

    current_version = DirectoryVersionSerializer(many=True)
    version = DirectoryVersionSerializer(many=True)

    class Meta:
        model = Directory
        fields = ('id', 'name', 'description', 'short_name', 'current_version', 'version')


class DirectoryDetailSerializer(serializers.ModelSerializer):
    """
    Справочник.
    """
    current_version = serializers.SerializerMethodField()
    version = DirectoryVersionSerializer(many=True)

    class Meta:
        model = Directory
        fields = ('id', 'name', 'description', 'short_name', 'current_version', 'version')

    def get_current_version(self, directory):
        version = DirectoryVersion.objects.filter(directory=directory).last()
        return DirectoryVersionSerializer(version).data
