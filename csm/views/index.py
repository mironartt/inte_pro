from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.views import generic
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from core.models.globals import Tile, Project
from ..forms.site_form import TileForm, TileEditForm


class IndexLoginAdminView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index_admin')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        return render(request, 'csm/authoricated.html',)

    def post(self, request, *args, **kwargs):
        context = {'error' : True}
        user = User.objects.filter(email=request.POST['username'], password=request.POST['password'])
        if user:
            auth.login(request, user=user.first())
            context['error'] = False
            return redirect('index_admin')

        print('request.user.is_authenticated >>>>>> 222. ' + str(request.user.is_authenticated))
        return render(request, 'csm/index.html', context)


class IndexAdminView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
        if not request.user.is_authenticated:
            return redirect('index_admin_login')

        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        context = {
            'tiles':Tile.objects.all()
        }

        return render(request, 'csm/index.html', context)



class TileEditView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
        if not request.user.is_authenticated:
            return redirect('index_admin_login')

        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        context = {
            'tile': Tile.objects.get(id=kwargs.get('pk')),
            'form': TileEditForm,
        }
        return render(request, 'csm/tile_edit.html', context=context)

    def post(self, request, *args, **kwargs):
        form = TileEditForm(request.POST, request.FILES)
        tile = Tile.objects.get(id=kwargs.get('pk'))
        context = {
            'form': form,
            'tile': tile,
        }
        if form.is_valid():
            tile.title = form.cleaned_data['title']
            tile.main_image = form.cleaned_data['main_image']
            tile.description = form.cleaned_data['description'].strip()
            tile.is_availabled = form.cleaned_data['is_availabled']
            tile.save()
            messages.success(request, 'Изменения плитки успешно сохранены')
            return redirect('admin_tile_edit', pk=tile.id)
        return render(request, 'csm/tile_edit.html', context)


class TileCreateView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
        if not request.user.is_authenticated:
            return redirect('index_admin_login')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'types': Tile.TYPE,
        }
        return render(request, 'csm/tile_create.html', context=context)

    def post(self, request, *args, **kwargs):
        form = TileForm(request.POST, request.FILES)
        context = {
            'types': Tile.TYPE,
            'form': form,
        }
        if form.is_valid():
            form.save()
            return redirect('index_admin_login')
        print('error >>> ' + str(form.errors))
        return render(request, 'csm/tile_create.html', context)



class TileOffView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
        if not request.user.is_authenticated:
            return redirect('index_admin_login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print('kwargs:  ' + str(kwargs))
        tile = Tile.objects.get(id=kwargs.get('pk'))
        tile.is_availabled = True if kwargs.get('action') == 1 else False
        tile.save()
        return redirect('index_admin')


def _logout(request):
    if not request.user.is_authenticated:
        return redirect('index_admin_login')
    else:
        auth.logout(request)
    return redirect('index_admin_login')