from django import forms
from .models import Post, Category
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
