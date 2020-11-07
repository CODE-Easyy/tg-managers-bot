from django.contrib import admin


from .models import Message, Client

admin.site.register(Message)
admin.site.register(Client)
