import json
import varenv
from PIL import Image, ImageDraw, ImageFont, ImageChops
from random import randint
from database import check_valentine, check_value, var_user, change_value
from uuid import uuid4

class LotOfLetters(Exception):
    pass
    
FONT_SIZE = 52
FONT = ImageFont.truetype('./adigiana.ttf', size=FONT_SIZE)
SPACING = -10
KISS_PATH = "./kiss.png"
KISS_WIDTH = 242
KISS_HEIGHT = 200

def upload_user_id(user_id):
    var_user(user_id)

def filling(draw, data):
    if data['align'] == 'left':
        minimal = 'stat'
        min_x = data['start_w']
        max_x = max(data['end_w'])
        dyn_w = data['end_w']
        stat_w = data['start_w']
    elif data['align'] == 'right':
        minimal = 'dyn'
        min_x = min(data['start_w'])
        max_x = data['end_w']
        dyn_w = data['start_w']
        stat_w = data['end_w']
    start_h = data['start_h']
    txt = ''
    for k in range(0, len(dyn_w)):
        txt += 'Съешь ещё этих мягких французских булок, да выпей же чаю'
        delta = draw.textsize(txt, spacing=SPACING, font=FONT)[1]
        end_h = data['start_h'] + int(delta)
        if minimal == 'stat':
            coords = (stat_w, start_h, dyn_w[k], end_h)
            draw.rectangle(coords, fill=(0, 0, 255, 255), outline=(0, 255, 0))
        elif minimal == 'dyn':
            coords = (dyn_w[k], start_h, stat_w, end_h)
            draw.rectangle(coords, fill=(0, 0, 255, 255), outline=(0, 255, 0))
        start_h = end_h
        txt += '\n'
    draw.rectangle((min_x, data['start_h'], max_x, data['end_h']), outline=(0, 255, 0), width=2)
    

def fill_space(draw, data):
    if data['partition'] == 1:
        end = 3
    elif data['partition'] == 0:
        end = 2
    for i in range(1, end):
        start_w = data[f'start_width{i}']
        end_w = data[f'end_width{i}']
        start_h = data[f'start_height{i}']
        end_h = data[f'end_height{i}']
        align = data[f'align{i}']
        num_rec = data[f'line_start{i}_recommend']
        input_data = {
            "start_w": start_w,
            "end_w": end_w,
            "start_h": start_h,
            "end_h": end_h,
            "align": align,
            "num_rec": num_rec
        }
        filling(draw, input_data)
    

def kiss(val_name, count=1, mask_name=''):
    img_bg = Image.open(f"{varenv.TEMP_FILES_DIR}/{val_name}")
    if mask_name == '':
        kissed_blank = Image.new("RGBA", img_bg.size, (0, 0, 0, 0))
    else:
        kissed_blank = Image.open(mask_path)
    im_kiss = Image.open(KISS_PATH)
    mask_kiss = im_kiss.resize((KISS_WIDTH, KISS_HEIGHT))
    w, h = img_bg.size
    blanks = []
    for i in range(0, count):
        empty_blank = Image.new("RGBA", img_bg.size, (0, 0, 0, 0))
        opacity = (randint(128, 255), randint(128, 255), randint(128, 255), randint(80, 128))
        opacity_im = Image.new("RGBA", (KISS_WIDTH, KISS_HEIGHT), opacity)
        mask = ImageChops.multiply(mask_kiss, opacity_im)
        x_kiss = randint(0, w - KISS_WIDTH) #randbelow(w-KISS_WIDTH)
        y_kiss = randint(0, h - KISS_HEIGHT) #randbelow(h-KISS_HEIGHT)
        empty_blank.paste(mask, (x_kiss, y_kiss))
        kissed_blank = Image.alpha_composite(kissed_blank, empty_blank)
    img_bg = img_bg.convert("RGBA")
    img_bg = Image.alpha_composite(img_bg, kissed_blank)
    if mask_name == '':
        mask_name = uuid4().hex + '.png'
        try:
            change_value("mask_temp_name", mask_name)
        except:
            return img_bg
    kissed_blank.save(f"{varenv.TEMP_FILES_DIR}/{mask_name}")
    img_bg.save(f"{varenv.TEMP_FILES_DIR}/{val_name}")

def lines_create(draw, input_data, txt, start_line=0):
    delta_h = input_data['delta_h']
    start_w = input_data['start_w']
    end_w = input_data['end_w']
    align = input_data['align']
    
    if align == 'left':
        dyn_w = end_w
        stat_w = start_w
    elif align == 'right':
        dyn_w = start_w
        stat_w = end_w
        
    w, h = draw.textsize(txt, spacing=SPACING, font=FONT)
        
    if h > delta_h:
        raise LotOfLetters
        
    lines = []
    for i in range(start_line, len(dyn_w)-1):
        delta_w = abs(dyn_w[i] - stat_w)
        if w > delta_w:
            delta_w1 = abs(dyn_w[i] - stat_w)
            delta_w2 = abs(dyn_w[i+1] - stat_w)
            deltas = [delta_w1, delta_w2]
            result = width_calc(draw, deltas, txt)
            if result[0] == 0:
                lines.append(result[1])
                lines.append(result[2])
                txt = ''
                break
            else:
                lines.append(result[1])
                txt = result[2]
        else:
            lines.append(txt)
            txt = ''
            break
        
    if txt != '':
        raise LotOfLetters
    else:
        lines_count = len(lines)
        txt = "\n".join(lines)
    txt_height = draw.textsize(txt, spacing=SPACING, font=FONT)[1]
        
    if txt_height > delta_h:
        raise LotOfLetters
    
    return {"count": lines_count, "text": txt}

def width_calc(draw, lines_width, txt):
    txt_splited = txt.split()
    word_count = len(txt_splited)
    
    if "От кого: " in txt:
        end = 1
    else:
        end = -1
    
    for j in range(word_count-1, end, -1):
        if "От кого: " in txt:
            first_line = "От кого: "
            first_line += " ".join([txt_splited[k] for k in range(2, j)])
        else:
            first_line = ""
            first_line += " ".join([txt_splited[k] for k in range(0, j)])
        second_line = ""
        second_line += " ".join([txt_splited[k] for k in range(j, word_count)])
        w1, h1 = draw.textsize(first_line, font=FONT)
        w2, h2 = draw.textsize(second_line, font=FONT)
        if w1 <= lines_width[0] and w2 <= lines_width[1]:
            return [0, first_line, second_line]
        elif w1 <= lines_width[0] and w2 > lines_width[1]:
            return [2, first_line, second_line]   

def height_calc(draw, line_number, start_h):
    test_line = ''
    for i in range(0, line_number):
        test_line += "Фа-фа"
        if i != line_number-1:
            test_line += "\n"
    height = draw.textsize(test_line, spacing=SPACING, font=FONT)[1]
    tolerance = 15
    return start_h + height - tolerance

def create_valentine(val_id, from_name="", to_name="", kiss_number=0, marks=False):
    data = dict(check_valentine(val_id))
    from_name = str(from_name)
    to_name = str(to_name)
    path = data["path"]
    if data['partition'] == 0:
        end = 2
    elif data['partition'] == 1:
        end = 3
    for i in range(1, end):
        if data[f'align{i}'] == 'left':
            data[f'end_width{i}'] = json.loads(data[f'end_width{i}'])
            data[f'start_width{i}'] = int(data[f'start_width{i}'])
        elif data[f'align{i}'] == 'right':
            data[f'start_width{i}'] = json.loads(data[f'start_width{i}'])
            data[f'end_width{i}'] = int(data[f'end_width{i}'])
    
    if from_name == "":
        from_bool, from_name = check_value(["from_standard", "from_text"])
        if from_bool == 1 and from_name == "":
            from_name = "От кого:\n"
        elif from_bool == 1 and from_name != "":
            from_name = "От кого: " + from_name
    else:
        if from_name == "":
            from_name = "От кого:\n"
        else:
            from_name = "От кого: " + from_name
        
    if to_name == "":
        to_bool, to_name = check_value(["to_standard", "to_text"])
        if to_bool == 1:
            to_name = "Кому: " + to_name
    else:
        to_name = "Кому: " + to_name
    
    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    
    if marks == True:
        fill_space(draw, data)
    
    if data['partition'] == 0:
        txt = ''
        start_recommend = data['line_start1_recommend'] - 1
        start_lines = [start_recommend, 0]
        y = 0
        for start in start_lines:
            if start != 0:
                min_h = data['start_height1']
                min_h_recommend = height_calc(draw, start, min_h)
                y = min_h_recommend
                max_h = data['end_height1']
                delta_h = max_h - min_h_recommend
                input_data = {
                        "delta_h": delta_h,
                        "start_w": data['start_width1'],
                        "end_w": data['end_width1'],
                        "align": data['align1']
                    }
            else:
                min_h = data['start_height1']
                y = min_h
                max_h = data['end_height1']
                delta_h = max_h - min_h
                input_data = {
                        "delta_h": delta_h,
                        "start_w": data['start_width1'],
                        "end_w": data['end_width1'],
                        "align": data['align1']
                    }        
                
            try:
                result_from = lines_create(draw, input_data, from_name, start)
                
                start_line = start + result_from['count']
                result_to = lines_create(draw, input_data, to_name, start_line)
                    
                txt = result_from['text'] + result_to['text']
                txt_height = draw.textsize(txt, spacing=SPACING, font=FONT)[1] + 30
                if txt_height > delta_h:
                    raise LotOfLetters
            except LotOfLetters:
                if start != 0:
                    print("Рекомендуемые условия не подходят")
                else:
                    print("Слишком много букв")
                    return False
            else:
                break
            
        align = data['align1']
        if align == "left":
            x1 = data["start_width1"]
            x2 = data["start_width1"]
        elif align == "right":
            w1 = draw.textsize(result_from['text'], spacing=SPACING, font=FONT)[0]
            x1 = data["end_width1"] - w1
            w2 = draw.textsize(result_to['text'], spacing=SPACING, font=FONT)[0]
            x2 = data["end_width1"] - w2
        color = data['color']
        draw.text((x1, y), result_from['text'], fill=color, font=FONT, spacing=SPACING, align=align)
        from_height = draw.textsize(result_from['text'], spacing=SPACING, font=FONT)[1]
        y = y + from_height
        draw.text((x2, y), result_to['text'], fill=color, font=FONT, spacing=SPACING, align=align)
        
    
    elif data['partition'] == 1:                
        color = data['color']
        txt = ''
        y1 = 0
        y2 = 0
        start_recommend1 = data['line_start1_recommend'] - 1
        start_recommend2 = data['line_start2_recommend'] - 1
        start_lines = [[start_recommend1, start_recommend2], 0]
        
        for start in start_lines:
            if type(start) == type([]) and (start[0] != 0 or start[1] != 0):
                start_from = start[0]
                min_h = data['start_height1']
                min_h_recommend = height_calc(draw, start_from, min_h)
                y1 = min_h_recommend
                max_h = data['end_height1']
                delta_h1 = max_h - min_h_recommend
                input_data_from = {
                        "delta_h": delta_h1,
                        "start_w": data['start_width1'],
                        "end_w": data['end_width1'],
                        "align": data['align1']
                    }
                
                start_to = start[1]    
                min_h = data['start_height2']
                min_h_recommend = height_calc(draw, start_to, min_h)
                y2 = min_h_recommend
                max_h = data['end_height2']
                delta_h2 = max_h - min_h_recommend
                input_data_to = {
                        "delta_h": delta_h2,
                        "start_w": data['start_width2'],
                        "end_w": data['end_width2'],
                        "align": data['align2']
                    }
                
            else:
                start_from = 0
                min_h = data['start_height1']
                y1 = min_h
                max_h = data['end_height1']
                delta_h1 = max_h - min_h
                input_data_from = {
                        "delta_h": delta_h1,
                        "start_w": data['start_width1'],
                        "end_w": data['end_width1'],
                        "align": data['align1']
                    }
                
                start_to = 0
                min_h = data['start_height2']
                y2 = min_h
                max_h = data['end_height2']
                delta_h2 = max_h - min_h
                input_data_to = {
                        "delta_h": delta_h2,
                        "start_w": data['start_width2'],
                        "end_w": data['end_width2'],
                        "align": data['align2']
                    }
                
                
            try:
                result_from = lines_create(draw, input_data_from, from_name, start_from)
                txt_from = result_from['text']
                txt_height = draw.textsize(txt_from, spacing=SPACING, font=FONT)[1] + 30
                if txt_height > delta_h1:
                    raise LotOfLetters
                    
                result_to = lines_create(draw, input_data_to, to_name, start_to)
                txt_to = result_to['text']
                txt_height = draw.textsize(txt_to, spacing=SPACING, font=FONT)[1] + 30
                if txt_height > delta_h2:
                    raise LotOfLetters
                    
            except LotOfLetters:
                if type(start) == type([]) and (start[0] != 0 or start[1] != 0):
                    print("Рекомендуемые условия не подходят")
                    
                else:
                    print("Слишком много букв")
                    return False
                    
            else:
                break
        
        align = data['align1']
        if align == "left":
            x1 = data["start_width1"]
        elif align == "right":
            width = draw.textsize(txt_from, spacing=SPACING, font=FONT)
            x1 = data["end_width1"] - width
        draw.text((x1, y1), txt_from, fill=color, font=FONT, spacing=SPACING, align=align)
        
        align = data['align2']
        if align == "left":
            x2 = data["start_width2"]
        elif align == "right":
            width = draw.textsize(txt_to, spacing=SPACING, font=FONT)[0]
            x2 = data["end_width2"] - width
        draw.text((x2, y2), txt_to, fill=color, font=FONT, spacing=SPACING, align=align)
    
    try:
        val_name = check_value('val_temp_name')[0]
    except:
        val_name = uuid4().hex + '.png'
        if str(kiss_number).isdigit():
            img.save(f"{varenv.TEMP_FILES_DIR}/{val_name}")
            kiss_count = abs(int(kiss_number))
            img = kiss(val_name, kiss_count)
        img.show()
    else:
        if val_name == None:
            val_name = uuid4().hex + '.png'
            change_value('val_temp_name', val_name)
        img.save(f"{varenv.TEMP_FILES_DIR}/{val_name}")
            
