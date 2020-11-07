from django.db import models

from django.contrib.auth import get_user_model
Manager = get_user_model()

TYPES = (
    ('sended', 'sended'),
    ('received', 'received')
)

class Client(models.Model):
    chat_id = models.PositiveIntegerField(
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    manager = models.ForeignKey(
        Manager, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    def __str__(self):
        return self.chat_id

class Message(models.Model):
    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )

    message = models.CharField(
        max_length=255
    )

    sended_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=255,
        choices=TYPES,
    )