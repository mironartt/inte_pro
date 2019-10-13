from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('', index.IndexAdminView.as_view(), name='index_admin'),
    path('login/', index.IndexLoginAdminView.as_view(), name='index_admin_login'),
    path('logout/', index._logout, name='index_admin_logout'),
    path('tile-create/', index.TileCreateView.as_view(), name='admin_tile_create'),
    path('tile-edit/<int:pk>', index.TileEditView.as_view(), name='admin_tile_edit'),
    path('tile-on/<int:pk>/<int:action>', index.TileOffView.as_view(), name='admin_tile_on'),
    path('tile-off/<int:pk>/<int:action>', index.TileOffView.as_view(), name='admin_tile_off'),
]