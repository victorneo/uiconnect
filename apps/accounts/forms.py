from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Field
from crispy_forms.bootstrap import FormActions


class LoginForm(forms.Form):
    username = forms.CharField(max_length=75, required=True)
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Login',
                'username',
                'password',
            ),
            FormActions(
                Submit('submit', 'Login', css_class='btn btn-primary')
            )
        )
        super(LoginForm, self).__init__(*args, **kwargs)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=75, required=True)
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput, help_text=u'Confirm your password.')
    bio = forms.CharField(max_length=400, required=False, widget=forms.Textarea)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Register',
                'username',
                'password',
                'password2',
                'bio',
                'avatar',
            ),
            FormActions(
                Submit('submit', 'Register', css_class='btn btn-primary')
            )
        )
        super(RegistrationForm, self).__init__(*args, **kwargs)
