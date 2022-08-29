import os
import random
from PIL import Image, ImageFont, ImageDraw

from io import BytesIO


def get_valid_pass(path:str, formats:list) -> list:
    all_files = os.listdir(path)
    valid_files = [file for file in all_files if file.split('.')[-1] in formats]
    return valid_files

# Путь к контенту
PATH_TO_PICTURE = "./pictures"
PATH_TO_FONTS = "./fonts"

# Переменные для хранения валидных картинок и шрифтов
VALID_PICTURE = get_valid_pass(PATH_TO_PICTURE, formats=['jpg', 'jpeg'])
VALID_FONTS = get_valid_pass(PATH_TO_FONTS, formats=['ttf', 'otf'])


def get_random_elements_for_picture():
    font = f"{PATH_TO_FONTS}/{random.choice(VALID_FONTS)}"
    picture = f"{PATH_TO_PICTURE}/{random.choice(VALID_PICTURE)}"
    return {
        "font": font,
        "picture": picture
    }

def draw_text_on_image(card_image, text, fontpath, color):
    """ Пишет/рисует текст на изображении с указанным фонтом и цветом"""
    font = ImageFont.truetype(fontpath, 70) # объект с фонтом
    draw = ImageDraw.Draw(card_image) # Объект для рисования
    x, y = card_image.size
    w, h = draw.textsize(text=text, font=font)
    # Вычисление центрирования текста по вертикали
    draw.text(((x-w) / 2, (y - h) / 2), text=text.upper(), font=font, fill=color, align='center')


def create_image(text_to_image:str, color="yellow"):
    """Собираем всё вместе, создаём холст и помещаем весь контент на него
    Каждый элемент словаря - это уже взятый рандомно экземпляр """
    picture_elements: dict = get_random_elements_for_picture()
    pic = Image.open(picture_elements['picture'])# .convert("RGBA") # todo чекнуть как без конверта сделать
    font = picture_elements['font']

    output_content = BytesIO() # Создаю объект класса, чтобы выгрузить пикчу в bites
    output_content.name = 'output_content.jpg'
    # Создаю холст
    card = Image.new("RGB", size=pic.size) # создал пустой холст
    card.paste(pic, (0, 0, pic.size[0], pic.size[1]))  # Закинул первым делом "основу" - саму пикчу
    draw_text_on_image(card_image=card, text=text_to_image, fontpath=font, color=color)

    card.save(output_content)
    output_content.seek(0)
    return output_content



# print(get_random_elements_for_picture())