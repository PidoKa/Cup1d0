import sqlite3
import json
import os
import varenv
from datetime import datetime

def new_print(line, user_id=None, logs_name='bot.log'):
    f = open(logs_name, 'a')
    now = datetime.now()
    if user_id != None:
        line = str(user_id) + ' ' + line
    new_line = now.strftime("%d/%m/%Y, %H:%M:%S") + ': ' + line + '\n'
    print(new_line)
    f.write(new_line)
    f.close()

def create_db():
    con = sqlite3.connect(varenv.varenv.DB_PATH)
    cur = con.cursor()

    cur.execute("CREATE TABLE users (user_id bigint default null, val_count int default 0, status tinyint default 0, val_id int default null, val_temp_name varchar(38) default null, mask_temp_name varchar(38), kisses_count int default 0, from_standard tinyint default 1, to_standard tinyint default 1, from_text text default '', to_text text default '', text_type tinyint default 0)")

    cur.execute("CREATE TABLE valentines (id int default null, type varchar(7) default NULL, path text default NULL, sent_count int default 0, available tinyint default 0, color varchar(20) default null, align1 varchar(6) default null, start_width1 varchar(255) default null, end_width1 varchar(255) default null, start_height1 int default 0, end_height1 int default 0, line_start1_recommend tinyint default 0, partition tinyint default 0, align2 varchar(6) default null, start_width2 varchar(255) default null, end_width2 varchar(255) default null, start_height2 int default 0, end_height2 int default 0, line_start2_recommend tinyint default 0)")

    con.commit()
    con.close()

def reload_patterns():
    con = sqlite3.connect(varenv.DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM valentines")
    patterns = []
    
    for json_path in varenv.JSON_PATHS:
        with open(json_path) as json_file:
            array = json.loads(json_file.read())
            for pattern in array:
                patterns.append(pattern)

    columns = ', '.join(patterns[0].keys())
    placeholders = ', '.join(['?'] * len(patterns[0].keys()))
    sql_query = f"INSERT INTO valentines ({columns}) VALUES ({placeholders})"
    last_id = 0
    
    for pattern in patterns:
        pattern['id'] = last_id
        values = list(pattern.values())
        cur.execute(sql_query, values)
        last_id += 1
        
    con.commit()  
    con.close()
