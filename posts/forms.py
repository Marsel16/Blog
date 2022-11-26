from django import forms

class PostCreateForm(forms.Form):
    title = forms.CharField(max_length=100, min_length=6)
    likes = forms.IntegerField()
class CommentCreateForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Введите текст комментария')
    # hashtag =
