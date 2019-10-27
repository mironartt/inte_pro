from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import index

urlpatterns = [
    path('', index.IndexView.as_view(), name='index'),
    path('site-block/', index.block_page, name='site_block'),
    path('site-sosi/', index.disable_block_page, name='disable_block_page'),
    path('site_artemis_open_site_sdsfeljdslfsdfjsdldsfjLDKJFLKjl/', index.available_block_page, name='available_block_page'),

]