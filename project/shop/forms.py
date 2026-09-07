from django.forms import ModelForm
from .models import Goods, Comment


class GoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = ('title', 'short_information', 'information', 'cost', 'rubric', 'photo_good')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )