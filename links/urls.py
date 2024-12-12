from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('link/<int:id>', views.card_view, name='card_view'),
]