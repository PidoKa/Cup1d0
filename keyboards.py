from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from database import check_value, check_valentine, var_user

def main_menu():
    keyboard = VkKeyboard()
    keyboard.add_button('Для моей половинки', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Для моего друга', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Мемную', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()
    
def add_text_menu(user_id):
    var_user(user_id)
    keyboard = VkKeyboard()
    columns = ["from_standard", "to_standard", "val_id", "from_text", "to_text"]
    from_template, to_template, val_id, from_text, to_text = check_value(columns)
    partition = check_valentine(val_id)['partition']
    
    if from_text == "" and to_text == "":
        action_from = "Добавить"
        action_to = "Добавить"
    elif from_text == "":
        action_from = "Добавить"
        action_to = "Изменить"
    elif to_text == "":
        action_from = "Изменить"
        action_to = "Добавить"
    else:
        action_from = "Изменить"
        action_to = "Изменить"
        
    if from_template == 0 and to_template == 0:
        if partition == 1:
            keyboard.add_button(f'{action_from} текст слева', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button(f'{action_to} текст справа', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        elif partition == 0:
            keyboard.add_button(f'{action_from} текст', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        button_from = ['Добавить "От кого"', VkKeyboardColor.POSITIVE] 
        button_to = ['Добавить "Кому"', VkKeyboardColor.POSITIVE] 
    elif from_template == 0:
        if partition == 1:
            keyboard.add_button(f'{action_from} текст слева', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        keyboard.add_button(f'{action_to} получателя', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        button_from = ['Добавить "От кого"', VkKeyboardColor.POSITIVE] 
        button_to = ['Удалить "Кому"', VkKeyboardColor.NEGATIVE] 
    elif to_template == 0:
        keyboard.add_button(f'{action_from} отправителя', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        if partition == 1:
            keyboard.add_button(f'{action_to} текст справа', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
        button_from = ['Удалить "От кого"', VkKeyboardColor.NEGATIVE] 
        button_to = ['Добавить "Кому"', VkKeyboardColor.POSITIVE]
    else:
        keyboard.add_button(f'{action_from} отправителя', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(f'{action_to} получателя', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        button_from = ['Удалить "От кого"', VkKeyboardColor.NEGATIVE] 
        button_to = ['Удалить "Кому"', VkKeyboardColor.NEGATIVE]
         
    keyboard.add_button(button_from[0], color=button_from[1])
    keyboard.add_line()
    keyboard.add_button(button_to[0], color=button_to[1])
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Далее', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()

def add_kiss_menu():
    keyboard = VkKeyboard()
    keyboard.add_button('Поцеловать', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Готово!', color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()
    
def get_value_menu():
    keyboard = VkKeyboard()
    keyboard.add_button("Назад", color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()
