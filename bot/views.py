from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response



from django.contrib.auth import get_user_model
Manager = get_user_model()


from .serializers import MessagesListSerializer
from .serializers import ClientsListSerializer
from .models import Message, Client
from .bot import bot

def get_client(chat_id):
    try:
        client = Client.objects.get(chat_id=chat_id)
        return client
    except:
        return None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    if request.method == 'POST':
        data = request.data

        client = get_client(data['client_chat_id'])

        if client:
            message = Message(
                manager=request.user,
                client=client,
                message=data['message'],
                status='sended'
            )
            message.save()
            bot.send_message(
                chat_id=data['client_chat_id'],
                text=data['message']
            )

            return Response(
                data={
                    'success': 'Message sent.', 
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={
                    'error': 'No client with such chat id.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            data={
                'error': "Only POST request\'s accepted."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def messages_list(request):
    if request.method == 'GET':
        messages = Message.objects.filter(
            manager__token=request.user.token
        ).filter(
            client__chat_id=request.data['client_chat_id']
        ).order_by('sended_at')

        serializer = MessagesListSerializer(messages, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            data={
                'error': "Only GET request\'s accepted."
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chats_list(request):
    if request.method == 'GET':
        clients = Client.objects.filter(
            manager__token=request.user.token,
        )
        serializer = ClientsListSerializer(clients, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            data={
                'error': "Only GET request\'s accepted."
            },
            status=status.HTTP_400_BAD_REQUEST
        )