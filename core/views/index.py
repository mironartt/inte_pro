import os
from django.conf import settings
from django.views import generic
from django.shortcuts import render, redirect, render_to_response, get_object_or_404

from ..models.globals import Tile, Project

class IndexView(generic.View):
    
    def dispatch(self, request, *args, **kwargs):
        if check_block():
            return redirect('site_block')

        print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
        if not request.user.is_superuser:
            return redirect('index_admin_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = {
            'tiles': Tile.objects.filter(is_availabled=True),
        }
        

        return render(request, 'core/index.html', context)



def block_page(request, *args, **kwargs):
    return render(request, 'block_site.html')

def disable_block_page(request, *args, **kwargs):
    file_action('create')
    return redirect('index')

def available_block_page(request, *args, **kwargs):
    file_action('remove')
    return redirect('index')

def file_action(action):
    base_dir = os.path.abspath(os.curdir)
    print('base L>>>> ' + str(base_dir))
    print('file >>>> ' + str(base_dir + 'block.txt'))
    if action == 'create':
        f = open(base_dir + 'block.txt', 'w')
        f.close()
    if action == 'remove':
        if os.path.exists(base_dir + 'block.txt'):
            os.remove(base_dir + 'block.txt')

def check_block():
    base_dir = os.path.abspath(os.curdir)
    if os.path.exists(base_dir + 'block.txt'):
        return True
    else:
        return False
