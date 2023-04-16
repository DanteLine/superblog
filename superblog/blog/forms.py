from django import forms
from blog.models import PostComment


class PostCommentForm(forms.ModelForm):
    context = forms.CharField(label='комментарий', widget=forms.Textarea(attrs={'class': 'form-control',
                                                         'rows': 5,
                                                         }))

    class Meta:
        model = PostComment
        fields = ['context',]


