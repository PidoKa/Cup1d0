import sqlite3
import os
import varenv
from random import randint

# status (users): 0 - меню, 1 - изменение текста, 2 - специальные эффекты, 3 - ввод какого-то текста
# type (valentines): 'lover', 'friend', 'memes'
# text_type (users): 0 - ввода текста нет, 1 - текст слева, 2 - текст справа, 3 - текст отправителя, 4 - текст получателя, 5 - ввод кол-ва поцелуев

def var_user(user_id):
    global user
    user = user_id

def find_user():
    con = sqlite3.connect(varenv.DB_PATH)
    cur = con.cursor()
    values = [user]
    cur.execute("SELECT * FROM users WHERE user_id=?", values)
    users_data = cur.fetchone()
    user_exist = True
    if users_data is None:
        cur.execute("INSERT INTO users (user_id) VALUES (?)", values)
        con.commit()
        user_exist = False
    con.close()
    return user_exist

def check_status():
    con = sqlite3.connect(varenv.DB_PATH)
    cur = con.cursor()
    values = [user]
    cur.execute("SELECT status FROM users WHERE user_id=?", values)
    data = cur.fetchone()
    return data[0]

def check_value(column_name):
    con = sqlite3.connect(varenv.DB_PATH)
    cur = con.cursor()
    values = [user]
    if type(column_name) == type([]):
        column_name = ', '.join(column_name)
    cur.execute(f"SELECT {column_name} FROM users WHERE user_id=?", values)
    data = cur.fetchone()
    return data
    
def change_value(column, value):
    con = sqlite3.connect(varenv.DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    values = [value, user]
    cur.execute(f"UPDATE users SET {column}=? WHERE user_id=?", values)
    con.commit()

def change_kisses_count(delta=1):
    con = sqlite3.connect(varenv.DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    values = [user]
    cur.execute("SELECT kisses_count FROM users WHERE user_id=?", values)
    data = cur.fetchone()
    if data['kisses_count'] > 100:
        return False
    new_count = data['kisses_count'] + delta
    values = [new_count, user]
    cur.execute("UPDATE users SET kisses_count=? WHERE user_id=?", values)
    con.commit()
    con.close()
    
def choose_val(val_type):
    con = sqlite3.connect(varenv.DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    values = [val_type]
    cur.execute("SELECT * FROM valentines WHERE type=?", values)
    data = cur.fetchall()
    
    flag = 0
    val = ''
    while flag == 0 and data != [] and data != None:
        val_num = randint(0, len(data)-1)
        val = data[val_num]
        flag = val['available']
        if flag == 0:
            del data[val_num]
    if data == [] or data == None:
        return None
    
    values = [user]
    cur.execute("SELECT val_count FROM users WHERE user_id=?", values)
    new_count = cur.fetchone()['val_count'] + 1
    
    values = [val['id'], new_count, user]
    cur.execute("UPDATE users SET val_id=?, val_count=? WHERE user_id=?", values)
    values = [val['sent_count']+1, val['id']]
    cur.execute("UPDATE valentines SET sent_count=? WHERE id=?", values)
    con.commit()
    con.close()
    return val['id']

def check_valentine(val_id):
    con = sqlite3.connect(varenv.DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    values = [val_id]
    cur.execute("SELECT * FROM valentines WHERE id=?", values)
    data = cur.fetchone()
    return data
  
def default():
    con = sqlite3.connect(varenv.DB_PATH)
    cur = con.cursor()
    values = [user]
    
    cur.execute("SELECT val_temp_name, mask_temp_name FROM users WHERE user_id=?", values)
    data = cur.fetchone()
    for i in range(0, 2):
        if data[i] != None:
            os.remove(f"{varenv.TEMP_FILES_DIR}/{data[i]}")
    
    cur.execute("UPDATE users SET val_count=0, status=0, val_id=null, val_temp_name=null, mask_temp_name=null, kisses_count=0, from_standard=1, to_standard=1, from_text='', to_text='', text_type=0 WHERE user_id=?", values)
    con.commit()
    con.close()
