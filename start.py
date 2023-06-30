import os
import varenv
from get_message import read_message
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from time import sleep
from send_message import default_message
from tools import create_db, reload_patterns, new_print

def main():
    vk_session = VkApi(token=varenv.ACCESS_TOKEN)
    longpoll = VkBotLongPoll(vk_session, varenv.GROUP_ID)
    vk = vk_session.get_api()
    if vk:
        new_print('Пульт управления работает...')
    
    new_print('Поехали!')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            new_print('Новое сообщение!')
            try:
                read_message(vk, event.obj)
            except Exception as err:
                default_message(vk, event.obj['message']['from_id'], "Произошла ошибка. Попробуйте снова позднее. Если ошибка повторится, то напишите аффтару, чтобы он выпил йаду.")
                new_print(f"ОШИБКА: {err}\nПерезапуск...")

if __name__ == '__main__':
    flag = True
    reg = 0
    while flag:
        print("----------------------------")
        print("Выберите действие:\n1 - Запустить бота.\n2 - (Пере)создать базу данных.\n3 - (Пере)загрузить настройки шаблонов.")
        print("----------------------------")
        answer = input()
        print("----------------------------")
        if answer.isdigit() and int(answer) in [1, 2, 3]:
            reg = int(answer)
            flag = False
        else:
            print("Пожалуйста, выберите действие")
            
    if reg == 1:
        while True:
            try:
                main()
            except Exception as err:
                sleep(3)
                new_print(f"ОШИБКА: {err}\nПерезапуск...")
                
    elif reg == 2:
        if os.path.isfile(varenv.DB_PATH):
            os.remove(varenv.DB_PATH)
        create_db()
        print(f"База данных {varenv.DB_PATH} создана.")
        
    elif reg == 3:
        if os.path.isfile(varenv.DB_PATH):
            reload_patterns()
            print(f"Шаблоны успешно (пере)загружены.")
        else:
            print(f"Шаблоны не обновлены, так как не существует базы данных. Пожалуйста, создайте базу данных!")
