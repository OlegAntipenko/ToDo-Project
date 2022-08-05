from django.contrib.auth.forms import UserCreationForm
from django import forms

from todo.models import User


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    job_title = forms.CharField(required=True, max_length=50)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "job_title", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.job_title = self.cleaned_data["job_title"]
        if commit:
            user.save()
        return user
