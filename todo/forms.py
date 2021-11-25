
from django import forms
from django.forms import fields
from todo.models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title", "state"]

    # def create_task(self):
    #     pass
