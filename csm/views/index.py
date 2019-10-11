from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from django.views import generic
from django.shortcuts import render, redirect, render_to_response, get_object_or_404



class IndexAdminView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        print('request.user.is_authenticated >>>>>>. ' + str(request.user.is_authenticated))
        if request.user.is_authenticated:
            pass

        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        context = {
            'test':'ZAEBUMBA!!!!!!!!!!!!!!!'
        }

        return render(request, 'csm/index.html', context)

    def post(self, request, *args, **kwargs):
        print('request.user.is_authenticated >>>>>>.  111' + str(request.user.is_authenticated))
        print('post >>>>>>> ' + str(request.POST))
        context = {'error' : True}
        print("request.POST['username'] >>>>>> " + str(request.POST['username']))
        print("request.POST['password'] >>>>>> " + str(request.POST['password']))
        user = User.objects.filter(email=request.POST['username'], password=request.POST['password'])
        print('users >>>>> ' + str(user))
        if user:
            auth.login(request, user=user.first())
            context['error'] = False

        print('request.user.is_authenticated >>>>>> 222. ' + str(request.user.is_authenticated))
        return render(request, 'csm/index.html', context)

