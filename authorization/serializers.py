from rest_framework import serializers

from django.contrib.auth import get_user_model
Manager = get_user_model()


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = (
            'id',
            'token',
            'name',
            'email',
        )