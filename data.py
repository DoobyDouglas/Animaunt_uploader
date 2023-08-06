import json
import os
from typing import Dict
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from config import write_config


PATHS = {}


def path_choice(
        title: str,
        master: tkinter.Tk = None,
        upload_bttn=None,
        ):
    if title == '':
        messagebox.showinfo('Нет названия', 'Введите название')
        return
    path = filedialog.askdirectory(title='Выберите папку с аниме')
    if path:
        bttn = master.nametowidget('add_ttl_frame.add_folder_bttn')
        bttn['text'] = 'Папка выбрана'
        bttn.config(bootstyle='success')
        PATHS[title] = path
        if upload_bttn:
            upload_bttn['text'] = 'Папка выбрана'
            upload_bttn.config(bootstyle='success')
    else:
        messagebox.showinfo('Ошибка', 'Папка не выбрана')
        return


def update_or_get_data(
        name: str = None,
        animaunt_link: str = None,
        findanime_link: str = None,
        anime_365_link: str = None,
        get: bool = False,
        master: tkinter.Tk = None,
        key: str = None,
        ) -> Dict or None:
    if not os.path.exists('anime.json'):
        with open('anime.json', 'w', encoding='utf-8') as json_file:
            data = {}
            json.dump(data, json_file)
    with open('anime.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if get:
        return data
    if not name:
        messagebox.showinfo('Нет названия', 'Введите название')
        return
    if not animaunt_link:
        messagebox.showinfo(
            'Нет ссылки',
            'Введите ссылку на Animaunt / Malfurik'
        )
        return
    if name not in data:
        if key == 'anime':
            data[name] = {
                'animaunt_link': animaunt_link,
                'findanime_link': findanime_link,
                'anime_365_link': anime_365_link,
            }
            if name in PATHS:
                data[name]['path'] = PATHS[name]
            else:
                data[name]['path'] = None
        elif key == 'dorama':
            data[name] = {
                'malfurik_link': animaunt_link,
                'doramatv_link': findanime_link,
            }
    with open('anime.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)
    if not get and master:
        master.nametowidget('add_ttl_frame.!entry').delete(0, 'end')
        master.nametowidget('add_ttl_frame.!entry2').delete(0, 'end')
        master.nametowidget('add_ttl_frame.!entry3').delete(0, 'end')
        master.nametowidget('add_ttl_frame.!entry4').delete(0, 'end')
        bttn = master.nametowidget('add_ttl_frame.add_folder_bttn')
        bttn.config(text='Выбрать папку')
        bttn.config(bootstyle='primary')
        try:
            master.nametowidget('.uploads_toplvl').destroy()
        except KeyError:
            pass


if __name__ == '__main__':
    pass