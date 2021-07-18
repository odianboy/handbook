from django.db import models


class Directory(models.Model):
    """
    Модель "Справочник".
    """
    name = models.CharField(max_length=120, verbose_name='Наименование')
    short_name = models.CharField(max_length=50, verbose_name='Короткое наименование')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return f'Справочник: {self.name} (id: {self.id})'


class DirectoryVersion(models.Model):
    """
    Модель "Версия справочника".
    """
    version = models.CharField(max_length=50, verbose_name='Версия')
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, verbose_name='Справочник', related_name='version')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата начала действия справочника')

    class Meta:
        unique_together = ('directory', 'version')
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

    def __str__(self):
        return f'Справочник: {self.directory.name} Версия: {self.version}'


class DirectoryItem(models.Model):
    """
    Модель "Элемент справочника".
    """
    directory_version = models.ForeignKey(
        DirectoryVersion,
        related_name='directory_item',
        on_delete=models.CASCADE,
        verbose_name='Версия справочника')
    code = models.CharField(max_length=50, null=False, verbose_name='Код элемента')
    element_value = models.CharField(max_length=50, null=False, verbose_name='Значение элемента')

    class Meta:
        unique_together = ('directory_version', 'code')
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочника'

    def __str__(self):
        return f'Код элемента: {self.code}'
