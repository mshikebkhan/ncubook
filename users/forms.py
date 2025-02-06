import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile, CoarseBranch
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



# The following usernames can't be used as username (they are forbidden).
forbidden_users = ['admin', 'html', 'password' 'edit', 'css', 'js', 'authenticate', 'login', 'logout',
                   'administrator', 'root', 'email', 'user', 'join', 'sql', 'static', 'python', 'delete']

class SignUpForm(UserCreationForm):
    """Sign Up form for new users."""
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Your Name", 'autofocus': '""'}), max_length=60, required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "A Unique Username", 'autocapitalize': "none", 'autocomplete': "username"}), max_length=30, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Password", 'autocomplete': "new-password"}), max_length=30, required=True)
    password2 = forms.CharField(required=False)

    class Meta: 
        model = User
        fields = ('first_name', 'last_name', 'username',
                'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

    def clean(self):

        # data from the form is fetched using super function
        super(SignUpForm, self).clean()

        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password1')
        username_list = list(username)
        periods_list = ['/', '"', "'", '!', '#', '*', '%',
                        '$', '^', '&', '(', ')', '+', ',', '?', '\\']

        # Conditions to be met for the username length.
        if username:

            # Conditions to be met for the username length.
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                    'Minimum 3 characters required'])

            if username in forbidden_users:
                self._errors['username'] = self.error_class([
                    'Invalid name for user, this is a reserverd word.'])

            for var in username:
                if var in periods_list:
                    self._errors['username'] = self.error_class([
                        'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])


        if name:
            if len(name) < 2:
                self._errors['name'] = self.error_class([
                    'Minimum 2 characters required.'])

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password1', e)

        # return any errors if found.
        return self.cleaned_data

class PasswordResetForm(forms.Form):
    otp = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Enter OTP"}))

    new_password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'input is-rounded is-link', 'placeholder': "New Password", 'autocomplete': "new-password"}), max_length=30, required=True)

    def clean(self):
        super(PasswordResetForm, self).clean()
        new_password = self.cleaned_data.get('new_password')

        if new_password:
            try:
                validate_password(new_password)
            except ValidationError as e:
                self.add_error('new_password', e)

        # return any errors if found
        return self.cleaned_data

class UserUpdateForm(forms.ModelForm):
    """Update user details."""
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "First Name"}), max_length=30, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Last Name"}), max_length=30, required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Username", 'autocapitalize': "none", 'autocomplete': "username"}), max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username','first_name' , 'last_name']

    def clean(self):

        # data from the form is fetched using super function
        super(UserUpdateForm, self).clean()

        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        username_list = list(username)
        periods_list = ['/','"', "'", '!', '#', '*', '%', '$', '^', '&', '(', ')', '+', ',', '?', '\\' ]


        if username:

            # Conditions to be met for the username length.
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                    'Minimum 3 characters required'])

            if username in forbidden_users:
                self._errors['username'] = self.error_class([
                    'Invalid name for user, this is a reserverd word.'])

            for var in username:
                if var in periods_list:
                    self._errors['username'] = self.error_class([
                        'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])

        if first_name:
            if len(first_name) < 2:
                self._errors['first_name'] = self.error_class([
                'Minimum 2 characters required'])   

        return self.cleaned_data

#Gender options
gender_choices = (
    ('Male','Male'),
    ('Female', 'Female'),
    )
 
class ProfileUpdateForm(forms.ModelForm):
    """Form to update/edit profile."""
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'file is-link'}))    
    gender = forms.ChoiceField(choices=gender_choices)
 
    roll = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Roll No."}))    
    year = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Academic Year"}))    
    birthday = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Ex- 01/01/2000"}, format='%d/%m/%Y'), input_formats=['%d/%m/%Y'], required=True)
    hometown = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Town/City"}),max_length=100, required=False)     
    interests = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input is-rounded is-link', 'rows': "7",
               'placeholder': "Interests/Hobbies", 'autocomplete': 'off'})
    , max_length=300, required=False)

    class Meta:
        model = Profile
        fields = ['coarse_branch' ,'profile_pic','roll', 'gender', 'year', 'birthday' , 'hometown', 'interests',]

    def clean(self):

        # data from the form is fetched using super function.
        super(ProfileUpdateForm, self).clean()

        roll = self.cleaned_data.get('roll').upper
        birthday = self.cleaned_data.get('birthday')

        # Sure for invalid birthdays.
        min_date = datetime.date(1900,1,1)
        max_date = datetime.date.today() - datetime.timedelta(days=365*12)
        if birthday:
            if birthday < min_date:
                self._errors['birthday'] = self.error_class([
                'Your age do not look real.'])
            if birthday > max_date:
                self._errors['birthday'] = self.error_class([
                'Your age must be at least 12.'])


        # return any errors if found
        return self.cleaned_data


class AccountVerifyForm(forms.Form):
    otp = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'input is-rounded is-link', 'placeholder': "Enter OTP"}))

class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'input is-rounded is-link', 'placeholder': "Current Password", 'autocomplete': "old-password", 'autofocus': "on"}), max_length=30, required=True)

    new_password = forms.CharField(widget=forms.PasswordInput(
    attrs={'class': 'input is-rounded is-link', 'placeholder': "New Password", 'autocomplete': "new-password"}), max_length=30, required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        user = User.objects.get(pk=id)

        if not user.check_password(old_password):
            self._errors['old_password'] =self.error_class(['Old password was incorrect.'])

        elif new_password:
            try:
                validate_password(new_password)
            except ValidationError as e:
                self.add_error('new_password', e)

        # return any errors if found
        return self.cleaned_data

