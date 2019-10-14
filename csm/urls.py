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
    path('tile-edit/project-edit/<int:tile_pk>/<int:project_pk>', index._project_edit, name='admin_project_edit'),
    path('tile-edit/project-remove/<int:project_pk>', index._project_remove, name='admin_project_remove'),
    path('tile-edit/project-create/<int:tile_pk>', index._project_create, name='admin_project_create'),
    path('tile-on/<int:pk>/<int:action>', index.TileOffView.as_view(), name='admin_tile_on'),
    path('tile-off/<int:pk>/<int:action>', index.TileOffView.as_view(), name='admin_tile_off'),
    path('dfgdgfdgsfdgfsdgfdgddsfejfhjhf4ff4ufh4k3fhkjfhj43fjkh43fkjn/', index._create_user, name='test_create_user'),
]