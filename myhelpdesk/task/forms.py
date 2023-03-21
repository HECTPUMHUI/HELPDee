from django import forms

from user.models import User
from .models import *


class AddTaskForm(forms.Form):
    title = forms.CharField(max_length=255, label="Task Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Description')
    completed = forms.BooleanField(required=False, initial=True, label='Completed')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Status', empty_label="Status not choised")
    user = forms.ModelChoiceField(queryset=User.objects.none(), empty_label="choise your user")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(id=user.id)

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'status', 'user']


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['text']
