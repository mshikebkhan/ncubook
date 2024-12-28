
from django import forms
from django.core.exceptions import ValidationError
from .models import Post



class PostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': "textarea has-fixed-size" ,'placeholder': "Share your thoughts with your NCU buddies", 'rows': "5", 'autocomplete': 'off', 'maxlength': "200", 'autofocus': 'on',}))

    url = forms.URLField(widget=forms.TextInput(attrs={'class': 'input is-small is-rounded', 'placeholder': "URL"}), required=False)

    pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'file is-link'}), required=False) 

    pdf = forms.FileField(widget=forms.FileInput(attrs={'class': 'file is-link', 'accept': '.pdf'}), required=False)

    class Meta:
        model = Post
        fields = ['body', 'url', 'pic', 'pdf']

    def clean(self):
        # data from the form is fetched using super function
        super(PostForm, self).clean()
        # return any errors if found.
        return self.cleaned_data



