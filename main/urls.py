# main/urls.py
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('send-chat/', views.send_chat, name='send_chat'),
    path('new-chat/', views.new_chat, name='new_chat'),
    path('delete-chat/', views.delete_chat, name='delete_chat'),
    path('rename-chat/', views.rename_chat, name='rename_chat'),
    path('chat-history/', views.get_chat_history, name='chat_history'),
    path('chat-detail/<str:chat_id>/', views.get_chat_detail, name='chat_detail'),
    path('book_plane/<str:plane_id>/', views.book_plane, name='book_plane'),
    path('book_hotel/<str:hotel_id>/', views.book_hotel, name='book_hotel'),
]