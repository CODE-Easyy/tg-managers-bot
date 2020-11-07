from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from django.contrib.auth import get_user_model
Manager = get_user_model()


from .serializers import ManagerSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    if request.method == 'GET':
        me = request.user
        serializer = ManagerSerializer(me)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            data={
                'error': 'Only GET request\'s accepted.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )