from django.conf import settings
from django.views import generic
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

from ..models.globals import Tile, Project

class IndexView(generic.View):

    def get(self, request, *args, **kwargs):
        context = {
            'tiles': Tile.objects.filter(is_availabled=True),
        }

        return render(request, 'core/index.html', context)
