from django.urls import path, include

from .views import (
    DirectoryListView,
    DirectoryDetailView,
    DirectoryItemListView
)

app_name = 'catalogs'

urlpatterns = [
    path('directories/', include([
        path('', DirectoryListView.as_view()),
        path('<int:pk>/', DirectoryDetailView.as_view()),
    ])),
    path('item/', DirectoryItemListView.as_view())
]
