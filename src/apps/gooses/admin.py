from django.contrib import admin
from django.forms import ModelForm
from .models import Goose


class GooseModelForm(ModelForm):
    class Meta:
        model = Goose
        exclude = ['update_time']

    def clean(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        return cleaned_data


class GooseAdmin(admin.ModelAdmin):
    form = GooseModelForm
    list_display = ['id', 'name', 'code', 'type', 'parent', 'update_time']
    list_editable = ['name', 'code', 'type', 'parent']


admin.site.register(Goose, GooseAdmin)
