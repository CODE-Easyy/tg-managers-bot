from django.urls import path


from . import bot

urlpatterns = [
    path('', bot.BotView.as_view()),
]
