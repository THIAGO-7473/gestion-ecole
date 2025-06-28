from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent_messages'),
    path('new/', views.new_message, name='new_message'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
] 