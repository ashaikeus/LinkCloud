from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('links/', views.filter_links, name='filter_links'),
    path('links/new/', views.create_link, name='links_new'),
    path('links/<int:pk>', views.link_view, name='link_view'),
    path('links/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('links/<int:pk>/save/', views.save_link, name='save_link'),
    path('links/<int:pk>/report/', views.report_link, name='report_link'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('register/', views.register, name='register'),
    path('users/<int:pk>', views.user_page, name='user_page'),
]