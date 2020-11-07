from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse 
from django.conf import settings
from django.contrib.auth import get_user_model
Manager = get_user_model()

from .models import Client, Message



import logging
import telebot
import time


WEBHOOK_HOST = 'tg-managers-bot.herokuapp.com'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = '/bot/'


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(settings.BOT_TOKEN)


def get_name(message):
    try:
        f_name = message.from_user.first_name
        return f_name
    except:
        return 'No name'


def get_or_create(message):
    chat_id = message.chat.id

    tg_client, is_created = Client.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            'name': get_name(message)
        }
    )
        
    return tg_client


def get_manager(token):
    try:
        manager = Manager.objects.get(token=token)
        return manager
    except:
        return None

    

@method_decorator(csrf_exempt, name='dispatch')
class BotView(View):
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        if request.headers.get('Content-Type') == 'application/json':
            json_string = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
        return HttpResponse('post')


@bot.message_handler(commands=['manager', 'start'])
def send_welcome(message):
    get_or_create(message)

    
    msg = bot.reply_to(message,
                 ('Hi!! Now please type token of you manager ......'))


    bot.register_next_step_handler(msg, wait_manager_token)

@bot.message_handler(content_types=['text'])
def chat_messages(message):
    try:
        client = get_or_create(message)
        new_message = Message()
        new_message.client = client
        new_message.manager = client.manager
        new_message.text = message.text
        new_message.status = 'received'
        new_message.save()
        bot.send_message(message.chat.id, 'Sended... Please wait till manager answer you.')
    except Exception as e:
        bot.send_message(message.chat.id, str(e))

def wait_manager_token(message):
    try:
        client = get_or_create(message)
        manager = get_manager(message.text)

        if not manager:
            msg = bot.send_message(
                message.chat.id,
                text='No manager with such token, please reenter...'
            )

            bot.register_next_step_handler(msg, wait_manager_token)
        else:
            client.manager = manager
            client.save()

            msg = bot.send_message(
                message.chat.id,
                text=f'You connected with {manager.name} manager. Now you can freely chat with him.'
            )
    except:
        msg = bot.send_message(
            message.chat.id,
            text='Something went wrong, please reenter token...'
        )

        bot.register_next_step_handler(msg, wait_manager_token)



bot.remove_webhook()
time.sleep(0.1)
bot.set_webhook(url=f'{WEBHOOK_URL_BASE}{WEBHOOK_URL_PATH}')