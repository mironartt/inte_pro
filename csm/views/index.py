from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.views import generic
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from core.models.globals import Tile, Project
from ..forms.site_form import TileForm, TileEditForm, ProjectCreateForm, CKEditorForm


def get_page_form(type, req=None):
    TYPE = (
        ('projects', ProjectCreateForm,),
        ('contacts', 'Контакты'),
        ('storage', 'Облачное хранилище'),
        ('requisites', 'Реквизиты'),
    )

    for types in TYPE:
        if types[0] == type:
            if not req:
                return types[1]
            else:
                return types[1](req)
    return None


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

        print('1111111111request.user.is_authenticated >>>>>> 222. ' + str(request.user.is_authenticated))
        return render(request, 'csm/authoricated.html', context)


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

##################################################################

class TileEditView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
        if not request.user.is_authenticated:
            return redirect('index_admin_login')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        tile = Tile.objects.get(id=kwargs.get('pk'))
        context = {
            'tile': tile ,
            'form': TileEditForm,
        }

        context['form_card'] = get_page_form(tile.type)
        context['projects'] = Project.objects.filter(tile_id=tile.id)
        context['ck_content'] = CKEditorForm()

        return render(request, 'csm/tile_edit.html', context=context)


    def post(self, request, *args, **kwargs):
        form = TileEditForm(request.POST, request.FILES)
        print('>>>>>>>>>> kwwwwargs >>> ' + str(kwargs))
        print('reFILE ================ ' + str(request.FILES))
        tile = Tile.objects.get(id=kwargs.get('pk'))
        context = {
            'form': form,
            'tile': tile,
            'projects': Project.objects.filter(tile_id=tile.id),
        }
        if form.is_valid():
            tile.title = form.cleaned_data['title']
            tile.main_image = form.cleaned_data['main_image']
            tile.description = form.cleaned_data['description'].strip()
            # tile.is_availabled = form.cleaned_data['is_availabled']
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


def _project_create(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('index_admin_login')
    print('_project_create >>>> kwargs >>> ' + str(kwargs))

    if request.method == 'POST':
        print('POST >>>>>>>>>>> ' + str(request.POST))

        tile = Tile.objects.get(id=kwargs.get('tile_pk'))
        if not tile.type == 'projects':
            messages.error(request, 'Ошибка в типе плитки')
            return redirect('admin_tile_edit', pk=tile.id)
        else:
            proj_form = get_page_form(tile.type, request.POST)

            if proj_form.is_valid():
                project = Project.objects.create(
                    tile_id=tile.id,
                    title=proj_form.cleaned_data['title'],
                    latitude=proj_form.cleaned_data['latitude'],
                    longitude=proj_form.cleaned_data['longitude'],
                    description=proj_form.cleaned_data['description'],
                )
                print('proj_form .>> NICE SAVE >>>>>>> ' + str(project.id))
                messages.success(request, 'Проект успешно создан')
                return redirect('admin_tile_edit', pk=tile.id)
            else:
                print('proj_form PIZDEC  <<< ' + str(proj_form.errors))
                messages.error(request, 'Ошибка при создание проекта. Проверьте правильность заполнения полей')
                return render(request, 'csm/tile_edit.html', {'tile':tile, 'form_card':proj_form, 'projects':Project.objects.filter(tile_id=tile.id), 'create_error':True,})




def _project_edit(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('index_admin_login')

    print('_project_edit >>>> kwargs >>> ' + str(kwargs))
    if request.method == 'POST':
        project = Project.objects.get(id=kwargs.get('project_pk'))
        tile = Tile.objects.get(id=kwargs.get('tile_pk'))
        proj_form = get_page_form(tile.type, request.POST)
        print('>>>>>>>>>> kwwwwargs >>> ' + str(kwargs))
        context = {
            'proj_form': proj_form,
            'tile': tile,
            'projects': Project.objects.filter(tile_id=tile.id),
        }
        if proj_form.is_valid():
            project.title = proj_form.cleaned_data['title']
            project.latitude = proj_form.cleaned_data['latitude']
            project.longitude = proj_form.cleaned_data['longitude']
            project.description = proj_form.cleaned_data['description']
            project.save()
            messages.success(request, 'Изменения проекта успешно сохранены')
            return redirect('admin_tile_edit', pk=tile.id)
        return render(request, 'csm/tile_edit.html', context)


def _project_remove(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('index_admin_login')

    print('_project_edit >>>> kwargs >>> ' + str(kwargs))
    project = Project.objects.get(id=kwargs.get('project_pk'))
    tile = Tile.objects.get(id=project.tile.id)
    project.delete()

    return redirect('admin_tile_edit', pk=tile.id)



def _create_user(request, *args, **kwargs):
    d = User.objects.create(
        username='test_admin_super',
        email='test_admin@mail.ru',
        password='qwerty',
        is_superuser=True
    )
    print('d >>>>>>>> =================== ' + str(d))

    return redirect('index_admin_login')