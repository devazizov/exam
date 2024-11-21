from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import PasswordInput
from django.forms import ModelForm
from django import forms


from django.contrib.auth import get_user_model

User = get_user_model()

class AddInputClass:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "text-dark form-control form-control-lg",
                    "placeholder": f"{field.label}",
                }
            )



class LoginForm(AddInputClass, AuthenticationForm):

    class Meta:
        model = User
        fields = ["email", "password"]


class RegistrationForm(AddInputClass, UserCreationForm):
    password1 = PasswordInput()
    password2 = PasswordInput()

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]



class AccountForm(AddInputClass, UserChangeForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label="New Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirm New Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
