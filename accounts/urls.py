from django.urls import path
from .views import become_author


urlpatterns = [
   path('author/', become_author, name='become_author'),
]
