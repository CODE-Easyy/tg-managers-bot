from django.urls import path


from . import bot
from . import views

urlpatterns = [
    path('bot/', bot.BotView.as_view()),
    path('send-message', views.send_message, name='send-message'),
    path('messages', views.messages_list, name='messages'),
    path('chats', views.chats_list, name='chats'),
]
