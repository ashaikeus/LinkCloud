from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('link/<int:pk>', views.link_view, name='link_view'),
    path('tags/<str:name>', views.tag_links, name='tag_links'),
]