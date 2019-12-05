#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import vk_api
import vk_api.bot_longpoll
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import sqlite3

# Сначала должен получить token
# Затем , должен авторизоваться
# Потом должен получить api

token_bot = '01b1cd2c6b7c0ecd3a08482786382b6263ed48f0dab8d76ae87697ae360b004d0780264314f1b7770ba35'
vk_ses = vk_api.VkApi(token=token_bot)

vk = vk_ses.get_api()

upload = VkUpload(vk_ses)
longpoll = VkLongPoll(vk_ses)

send_vk = vk.messages.send

bio = ('Мой создатель - Борис Кузнецов\n'
       ' \n'
       ' Студент 1 курса НГУ Экономического Факультета отделения Бизнес- Информатика\n'
       ' \n'
       ' Этот бот был разработан им, как  большой проект , для предмета программирования ')

keyboard = VkKeyboard(one_time=True)

keyboard.add_button('Мой создатель', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Поддержать проект', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Получить id', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('Как это работает?', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Есть ли в боте этот человек?', color=VkKeyboardColor.NEGATIVE)

about_bot = ('Этот бот позволяет отправлять людям анонимные сообщения\n'
             '\n'
             'И они не будут знать кто это им отправил\n'
             '\n'
             'Да, есть небольшая загвоздка(\n'
             'Бот не может отправить сообщение людям\n'
             'Которые еще заходили в него\n'
             '(я надеюсь , что придумаю как это можно обойти)\n'
             '\n'
             'Так что скорее зови друзей ,\n'
             'И отсылай им свои анонимки)')

session = requests.Session()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        print('id{}: "{}"'.format(event.user_id, event.text), end=' ')
        name_o = vk.users.get(user_ids=event.user_id, fields='city')
        your_name = ((str(name_o)).split(" ")[3]).replace("'", '').replace(',', '')
        # city_o = ((str(name_o)).split(" ")[14]).replace("'", '').replace(',', '').replace('}', '').replace(']', '')
        print(your_name)

        #Тестовое сообщение
        if event.text == 'hello':
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message='Whats up')

        #Информация о создателе бота
        elif event.text == 'Мой создатель':
            photo = vk.users.get(user_id=event.user_id, fields='photo_max_orig')
            photo_id = vk.users.get(user_id=event.user_id, fields='photo_id')
            print(photo_id)
            print(photo)
            photo = str(photo)
            p_s = photo.split(' ')
            ava = p_s[11]
            ava_not = ava[1:ava.rfind("?")]
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=bio,
                             attachment='photo558924310_457239018', keyboard=keyboard.get_keyboard())

        #Вкладка поддержать проект
        elif event.text == 'Поддержать проект':
            message = (
                'Чтобы поддержать прект, переведите сюда рублик и укажите свой ID, ваш  ID: ' + str(event.user_id)
                , '\nmoney.yandex.ru/to/410017167191435')
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=message
                             , keyboard=keyboard.get_keyboard())

        elif str(event.text).startswith('send/'):
            y = str(event.text).split('/')
            print(y[1])
            try:
                vk.messages.send(user_id=y[1], random_id=get_random_id(), message=y[2],
                                 keyboard=keyboard.get_keyboard())
                vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message='Отправленно!'
                                 , keyboard=keyboard.get_keyboard())
            except vk_api.exceptions.ApiError:
                vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                 message='Я не могу отправить сообщение этому пользвотелю, подожди, пока он напишет, '
                                         'хоть что-то этому боту',
                                 keyboard=keyboard.get_keyboard())

        elif event.text == 'Как это работает?':
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                             message="Вы просто должны должны отправить боту сообщние боту как \n  'send/id польователя(тут обязательно цифры, которые ты можешь получить, нажав на Получить id)/ваше сообщение' например:"
                             , keyboard=keyboard.get_keyboard())
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                             message="send/558924310/Hi!"
                             , keyboard=keyboard.get_keyboard())

        elif event.text == 'Получить id':
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                             message='Просто отправь ссылку пользователя нам'
                             , keyboard=keyboard.get_keyboard())


        elif str(event.text).startswith('htt') or str(event.text).startswith('www') or str(event.text).startswith('vk'):
            try:
                if str(event.text).find('id') != -1:
                    short_id_have = str(event.text)[str(event.text).find('id') + 2:]
                    print(short_id_have)
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                     message=short_id_have
                                     , keyboard=keyboard.get_keyboard())

                else:
                    short_id = str(event.text)[str(event.text).find('com/') + 4:]
                    print(short_id)
                    ne_short = vk.users.get(user_ids=short_id, fields='photo_id')
                    id_split = str(ne_short).split(' ')
                    id_no = id_split[1].replace(',', '')
                    # aaaaa = str(id_no)[1:id_no.find("'")]
                    print(id_no)
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                     message=id_no
                                     , keyboard=keyboard.get_keyboard())
            except vk_api.exceptions.ApiError:
                vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                 message='Неправильная ссылка пользователя'
                                 , keyboard=keyboard.get_keyboard())

        elif event.text == 'Об этом боте':
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                             message=about_bot
                             , keyboard=keyboard.get_keyboard())

        elif event.text == 'Есть ли в боте этот человек?':
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                             message="отправь ссылку на человека и вначале добавь этот знак *"
                             , keyboard=keyboard.get_keyboard())


        elif str(event.text).startswith('*'):
            ok = str(event.text).replace('*', '').replace(' ', '')
            if str(ok).startswith('htt') or str(ok).startswith('www') or str(ok).startswith('vk'):
                try:
                    if str(ok).find('id') != -1:
                        short_id_have = str(ok)[str(ok).find('id') + 2:]
                        print(short_id_have)
                        # vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                        # message=short_id_have
                        # , keyboard=keyboard.get_keyboard())

                        try:
                            vk.messages.send(user_id=short_id_have, random_id=get_random_id(),
                                             message='Вам хотят отправить Анонимку!'
                                             , keyboard=keyboard.get_keyboard())
                            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                             message='Это пользователю можно отправить анонимку',
                                             keyboard=keyboard.get_keyboard())

                        except vk_api.exceptions.ApiError:
                            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                             message='Этому пользователю мы не можем отправить Анонимку('
                                             , keyboard=keyboard.get_keyboard())
                    else:
                        short_id = str(ok)[str(ok).find('com/') + 4:]
                        print(short_id)
                        ne_short = vk.users.get(user_ids=short_id, fields='photo_id')
                        id_split = str(ne_short).split(' ')
                        id_no = id_split[1].replace(',', '')
                        # aaaaa = str(id_no)[1:id_no.find("'")]
                        print(id_no)
                        # vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                        # message=id_no
                        # , keyboard=keyboard.get_keyboard())
                        try:
                            vk.messages.send(user_id=id_no, random_id=get_random_id(),
                                             message='Вам хотят отправить Анонимку!'
                                             , keyboard=keyboard.get_keyboard())
                            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                             message='Это пользователю можно отправить анонимку',
                                             keyboard=keyboard.get_keyboard())
                        except vk_api.exceptions.ApiError:
                            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                             message='Этому пользователю мы не можем отправить Анонимку('
                                             , keyboard=keyboard.get_keyboard())
                except vk_api.exceptions.ApiError:
                    vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                     message='Неправильная ссылка пользователя'
                                     , keyboard=keyboard.get_keyboard())





        else:
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                             message='Не такой команды, выбирите другую'
                             , keyboard=keyboard.get_keyboard())
