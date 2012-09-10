from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Field
from crispy_forms.bootstrap import FormActions


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=75, required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('username', css_class='span6'),
            ),
            FormActions(
                Submit('submit', 'Send new password', css_class='btn btn-primary')
            )
        )
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=75, required=True)
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
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
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.PasswordInput,
        label=u'Password Again',
        help_text=u'Confirm your password.'
    )
    bio = forms.CharField(max_length=400, required=False, widget=forms.Textarea)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('username', css_class='span6'),
                Field('email', css_class='span6'),
                Field('password', css_class='span6'),
                Field('password2', css_class='span6'),
                Field('bio', css_class='span6'),
                Field('avatar', css_class='span6'),
            ),
            FormActions(
                Submit('submit', 'Register', css_class='btn btn-primary')
            )
        )
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password', '')
        password2 = cleaned_data.get('password2', '')

        if password != password2:
            msg = u'Passwords are not the same.'
            self._errors['password'] = self.error_class([msg])
            self._errors['password2'] = self.error_class('')

            del cleaned_data['password']
            del cleaned_data['password2']

        # Always return the full collection of cleaned data.
        return cleaned_data


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.PasswordInput,
        help_text='Leave empty if you do not want to change password.'
    )
    password2 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.PasswordInput,
        label=u'Password Again',
    )
    bio = forms.CharField(max_length=400, required=False, widget=forms.Textarea)
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('name', css_class='span6'),
                Field('email', css_class='span6'),
                Field('password', css_class='span6'),
                Field('password2', css_class='span6'),
                Field('bio', css_class='span6'),
                Field('avatar', css_class='span6'),
            ),
            FormActions(
                Submit('submit', 'Update', css_class='btn btn-primary')
            )
        )
        super(ProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        password = cleaned_data.get('password', '')
        password2 = cleaned_data.get('password2', '')

        if password != password2:
            msg = u'Passwords are not the same.'
            self._errors['password'] = self.error_class([msg])
            self._errors['password2'] = self.error_class('')

            del cleaned_data['password']
            del cleaned_data['password2']

        # Always return the full collection of cleaned data.
        return cleaned_data
