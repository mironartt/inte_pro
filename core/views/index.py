from django.conf import settings
from django.views import generic
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

from ..models.globals import Tile, Project

class IndexView(generic.View):
    
    # def dispatch(self, request, *args, **kwargs):
    #     print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
    #     if not request.user.is_superuser:
    #         return redirect('index_admin_login')
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = {
            'tiles': Tile.objects.filter(is_availabled=True),
        }
        

        return render(request, 'core/index.html', context)
