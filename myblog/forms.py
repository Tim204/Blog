from django import forms
from myblog.models import Comment

class BlogPostEmailForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'name': '',
            'email': '',
            'body': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name:'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email address:'}),
            'body': forms.Textarea(attrs={'placeholder': 'Comment'})
        }
