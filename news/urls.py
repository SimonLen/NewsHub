from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostAddView, PostDeleteView, PostEditView, CategoryPostsList, subscribe


urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>', PostDetail.as_view()),
   path('search/', PostSearch.as_view()),
   path('add/', PostAddView.as_view(), name='post_add'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
   path('edit/<int:pk>', PostEditView.as_view(), name='post_edit'),
   path('categories/<int:pk>', CategoryPostsList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
]
