from keyboards import *
from database import *
from send_message import *
from valentine import create_valentine, kiss
from random import randint
from tools import new_print

jokes = [
    'Сижу, реву. Мой муж утирает мне слёзы. Я подумала, что это так мило. Подхожу к зеркалу… эта сволочь мне расплывшейся тушью усы пририсовала.',
    'Учительница географии попросила Иванова показать Рим, и уже вечером пара, бросив всё, мчалась в город любви.',
    'Директор ЖКХ влюбился, но так и не смог дарить тепло.',
    'Давно хочу сказать «Я люблю тебя», но всё время некому.',
    '- Из-за чего ты меня полюбил?\n- Из-за глаз!\n- Тебе сразу понравились мои глаза?\n- Нет, просто у меня зрение плохое.',
    ]
    
def read_message(vk, obj):
    obj = obj['message']
    user_id = obj['from_id']
    var_user(user_id)
    text = obj['text']

    if find_user() == False:
        default_message(vk, user_id, '[ УСТАНОВЛЕНО СОЕДИНЕНИЕ С АБОНЕНТОМ: cup1d0n_l0v3_m4ch1n3 ]')
        keyboard_message(vk, user_id, 'Привет! Я тот пацан со стрелой, из-за которого случились многие великие трагедии и великие комедии! Сегодня 14 февраля — день, чтобы порадовать близких вам людей вниманием или признаться кому-то, к кому вы неравнодушны, в любви! Я подготовил прекрасные валентинки, которые помогут в этом нелёгком деле.', main_menu())
    
    elif check_status() == 0:
        if text == 'Для моей половинки':
            val_id = choose_val('lover')
            if val_id == None:
                answer = 'В данный момент таких валентинок нет.'
                default_message(vk, user_id, answer)
                return None
            else:
                answer = 'О, это прекрасно! Если ты только признаёшься — держу за тебя кулачки (а точнее — лук со стрелами).'
        elif text == 'Для моего друга':
            val_id = choose_val('friend')
            if val_id == None:
                answer = 'В данный момент таких валентинок нет.'
                default_message(vk, user_id, answer)
                return None
            else:
                answer = 'Замечательно, что у тебя есть такие друзья, которым ты доверяешь и веришь так, как себе.'
        elif text == 'Мемную':
            val_id = choose_val('memes')
            if val_id == None:
                answer = 'В данный момент таких валентинок нет.'
                default_message(vk, user_id, answer)
                return None
            else:
                i = randint(0, 4)
                answer = 'Кхм... Анекдот! ' + jokes[i]
        create_valentine(val_id)
        
        val_name = check_value("val_temp_name")[0]
        photo = photo_upload(vk, f"{varenv.TEMP_FILES_DIR}/{val_name}")
        change_value('status', 1)
        default_message(vk, user_id, answer)
        keyboard_message(vk, user_id, 'Вот твоя валентинка! Ты можешь её настроить с помощью кнопок.', add_text_menu(user_id), photo)
        
    elif check_status() == 1:
        if text == 'Назад':
            default()
            keyboard_message(vk, user_id, "Выберите вид валентинки", main_menu())
        elif text in ["Добавить отправителя", "Изменить отправителя", "Добавить текст слева", "Изменить текст слева", "Добавить текст", "Изменить текст"]:
            if "Изменить" in text:
                answer = "Ваш прошлый текст:\n\n" + check_value("from_text")[0]
            else:
                answer = "Введите текст, который вы хотите увидеть на валентинке:"
            change_value("status", 3)
            change_value("text_type", 1)
            keyboard_message(vk, user_id, answer, get_value_menu())
        elif text in ["Добавить получателя", "Изменить получателя", "Добавить текст справа", "Изменить текст справа"]:
            if "Изменить" in text:
                answer = "Ваш прошлый текст:\n\n" + check_value("to_text")[0]
            else:
                answer = "Введите текст, который вы хотите увидеть на валентинке:"
            change_value("status", 3)
            change_value("text_type", 2)
            keyboard_message(vk, user_id, answer, get_value_menu())
        elif text in ['Удалить "От кого"', 'Добавить "От кого"']:
            if "Удалить" in text:
                value = 0
            elif "Добавить" in text:
                value = 1
            change_value("from_standard", value)
            val_id = check_value('val_id')[0]
            create_valentine(val_id)
            val_name = check_value("val_temp_name")[0]
            photo = photo_upload(vk, f"{varenv.TEMP_FILES_DIR}/{val_name}")
            keyboard_message(vk, user_id, keyboard=add_text_menu(user_id), attachment=photo)
        elif text in ['Удалить "Кому"', 'Добавить "Кому"']:
            if "Удалить" in text:
                value = 0
            elif "Добавить" in text:
                value = 1
            change_value("to_standard", value)
            val_id = check_value('val_id')[0]
            create_valentine(val_id)
            val_name = check_value("val_temp_name")[0]
            photo = photo_upload(vk, f"{varenv.TEMP_FILES_DIR}/{val_name}")
            keyboard_message(vk, user_id, keyboard=add_text_menu(user_id), attachment=photo)
        elif text == "Далее":
            change_value("status", 2)
            keyboard_message(vk, user_id, 'Открытка почти готова. Осталось дело за малым: ты можешь привнести немного романтики на открытку, поцеловав её. Результат отобразится после нажатия на кнопку "Готово".', add_kiss_menu())
    
    elif check_status() == 2:
        if text == "Поцеловать":
            change_kisses_count()
            mid = str(obj['id'])
            pid = str(obj['peer_id'])
            vk.messages.markAsRead(peer_id=pid)
        elif text == "Готово!":
            val_name, kisses_count = check_value(["val_temp_name", "kisses_count"])
            kiss(val_name, kisses_count)
            photo = photo_upload(vk, f"{varenv.TEMP_FILES_DIR}/{val_name}")
            keyboard_message(vk, user_id, "Получите и распишитесь (в ЗАГСе)!", keyboard=main_menu(), attachment=photo)
            default()
        elif text == "Назад":
            change_value("status", 1)
            answer = "Здесь вы можете настроить текстовое оформление валентинки."
            keyboard_message(vk, user_id, answer, add_text_menu(user_id))

    elif check_status() == 3:
        if text != "Назад":
            text_type = check_value("text_type")[0]
            if text_type == 1:
                change_value("from_text", text)
            elif text_type == 2:
                change_value("to_text", text)
            val_id = check_value("val_id")[0]
            val_flag = create_valentine(val_id)
            if val_flag == False:
                default_message(vk, user_id, "Пожалуйста, уменьшите ваш текст: в нём слишком большие слова или слишком много букв.")
                return None
            val_name = check_value("val_temp_name")[0]
            photo = photo_upload(vk, f"{varenv.TEMP_FILES_DIR}/{val_name}")
            answer = None
        else:
            photo = None
            answer = "Здесь вы можете настроить текстовое оформление валентинки."
        change_value("status", 1)
        change_value("text_type", 0)
        keyboard_message(vk, user_id, answer, add_text_menu(user_id), photo)         
            
    else:   
        default_message(vk, user_id, 'Такой команды не существует. Пожалуйста, воспользуйтесь клавиатурой!')

    new_print('Я ответил ' + vk.users.get(user_ids=user_id, name_case='dat')[0]['first_name'])
    return True
