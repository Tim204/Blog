from django import forms
from myblog.models import Comment


class BlogPostEmailForm(forms.Form):
    # label="" to prevent default field name from rendering on the template
    name = forms.CharField(max_length=25, label="",  widget=forms.TextInput(
        attrs={"placeholder": 'Your Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={"placeholder": 'Your Email Adress'}))
    to = forms.EmailField(label="", widget=forms.TextInput(
        attrs={"placeholder": "To: Reciever's Email Adress"}))
    comments = forms.CharField(required=False, label="",
                               widget=forms.Textarea(attrs={"placeholder": 'Comments'}))


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
