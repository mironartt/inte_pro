from django import forms
from core.models.globals import Tile, Project
from ckeditor.widgets import CKEditorWidget


class TileForm(forms.ModelForm):

    type = forms.CharField(max_length=20, required=True,)
    title = forms.CharField(max_length=100, required=True,)
    description = forms.CharField(max_length=130, required=True,)
    main_image = forms.FileField()

    class Meta(object):
        model = Tile
        fields = ['type', 'title', 'main_image', 'description']

class TileEditForm(forms.ModelForm):

    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=130)
    main_image = forms.FileField(required=False)
    is_availabled = forms.BooleanField(required=False)

    class Meta(object):
        model = Tile
        fields = ['title', 'main_image', 'description', 'is_availabled']


class ProjectCreateForm(forms.ModelForm):

    title = forms.CharField(max_length=100, required=True,)
    # main_image = forms.FileField()
    description = forms.Textarea()
    latitude = forms.DecimalField(max_digits=10, decimal_places=6, required=True)
    longitude = forms.DecimalField(max_digits=10, decimal_places=6, required=True)

    class Meta(object):
        model = Project
        fields = ['title', 'description', 'latitude', 'longitude', ]


class CKEditorForm(forms.Form):

    content = forms.CharField(widget=CKEditorWidget())