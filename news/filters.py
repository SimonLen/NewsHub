from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from django.contrib.auth.models import User
from django import forms
from .models import Post


class PostFilter(FilterSet):
    date = DateFilter(field_name='creation_date', widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='gte', label='Дата публикации ранее, чем')
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок содержит')
    author = ModelChoiceFilter(field_name='author__user__username', label='Автор', queryset=User.objects.all())

    class Meta:
        model = Post
        fields = [
            'date',
            'title',
            'author',
        ]
