import asyncio
import datetime
import os
import random
import time
from multiprocessing import Process

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'Tg_rare_bot.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from Models.models import Rare, Message, API, System, SendMessage
from telethon.sync import TelegramClient
from telethon.tl.functions import account


def check_24_hour():
    while True:
        all_api = API.objects.filter(can_send_message=False)
        for api in all_api:
            if api.has_24_hours_passed:
                api.can_send_message = True
                api.save()
        time.sleep(15 * 60)


async def bot_status_update():
    while True:
        random_diapasine = random.randint(25, 100)
        all_api = API.objects.filter(is_activate=True)
        for api in all_api:
            username = api.username
            phone = api.phone
            api_id = int(api.api_id)
            api_hash = api.api_hash
            if random.randint(0, 100) <= random_diapasine:
                client = TelegramClient(username, api_id=api_id, api_hash=api_hash, system_version="4.16.30-vxCUSTOM")
                await client.start(phone=phone)
                await client(account.UpdateStatusRequest(offline=False))
                await client.disconnect()
        time.sleep(295)


async def activate_sessions(all_api):
    for api in all_api:
        username = api.username
        phone = api.phone
        print(phone)
        api_id = int(api.api_id)
        api_hash = api.api_hash
        client = TelegramClient(username, api_id=api_id, api_hash=api_hash, system_version="4.16.30-vxCUSTOM")
        await client.start(phone=phone)
        await client.disconnect()


async def send_message_to_users(api, message):
    client = TelegramClient(api.username, api_id=api.api_id, api_hash=api.api_hash, system_version="4.16.30-vxCUSTOM")
    await client.start(phone=api.phone)
    time.sleep(5)
    await client.send_message(entity='@easychatP2P',
                              message=message.text)
    client.disconnect()
    SendMessage.objects.create(message=message)
    api.can_send_message = False
    api.last_send_message = datetime.datetime.now()
    api.save()


async def main():
    p1 = Process(target=check_24_hour)
    p1.start()
    task = input(
        'Вы уже актевировали сессии? Если нет, то введите 1, если акстивировали, но хотите внесли новые номера, нажмите 2, иначе введите любой символ\n')
    normal_use = 0
    offen_use = 2
    if task == '1':
        all_api = API.objects.all()
        await activate_sessions(all_api)
    elif task == '2':
        all_api = API.objects.filter(is_activate=False)
        await activate_sessions(all_api)
    await bot_status_update()
    while True:
        minimum = System.objects.get(id=1).min
        maximum = System.objects.get(id=1).max
        need_sleep = random.randint(minimum, maximum)
        # if normal_use == 2 and offen_use == 4:
        #   rare = Rare.objects.get(name='Rare')
        #  normal_use = 0
        # offen_use = 0
        # elif (offen_use == 2 and normal_use == 0) or (normal_use == 1 and offen_use == 4):
        #   rare = Rare.objects.get(name='Normal')
        #  normal_use += 1
        # else:
        #   rare = Rare.objects.get(name='Frequent')
        #  offen_use += 1
        message = random.choice(Message.objects.all())
        try:
            api = random.choice(API.objects.filter(can_send_message=True))
            print(api.phone)
            await send_message_to_users(api=api, message=message)
            time.sleep(need_sleep * 60)
        except Exception:
            print('Нет подходящих пользователей')
            time.sleep(120)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
