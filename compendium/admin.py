from django.contrib import admin
from .models import Directory, DirectoryItem, DirectoryVersion
from django.contrib.auth.models import User, Group

admin.site.unregister([User, Group])


class DirectoryItemInline(admin.TabularInline):
    model = DirectoryItem
    extra = 1


class DirectoryVersionInline(admin.TabularInline):
    model = DirectoryVersion
    extra = 1


@admin.register(Directory)
class AdminDirectory(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'short_name',
        'description',
    )
    list_filter = (
        'name',
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    inlines = [DirectoryVersionInline]


@admin.register(DirectoryVersion)
class AdminDirectoryVersion(admin.ModelAdmin):
    list_display = (
        'id',
        'version',
        'directory',
        'created_date'
    )
    list_filter = (
        'directory',
        'version'
    )
    search_fields = ('version', 'directory')
    list_display_links = ('version', 'directory', 'created_date')

    inlines = [DirectoryItemInline]


@admin.register(DirectoryItem)
class AdminDirectoryItem(admin.ModelAdmin):
    list_display = (
        'id',
        'directory_version',
        'code',
        'element_value',
    )
    list_filter = (
        'directory_version',
        'code',
    )
    search_fields = ('code', 'directory_version')
    list_display_links = ('directory_version', 'code', 'element_value')
