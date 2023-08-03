import json
import os
from pprint import pprint
from typing import Dict
import tkinter


def update_or_get_data(
        name: str = None,
        animaunt_link: str = None,
        findanime_link: str = None,
        get: bool = False,
        master: tkinter.Tk = None,
        ) -> Dict or None:
    if not os.path.exists('anime.json'):
        with open('anime.json', 'w', encoding='utf-8') as json_file:
            data = {}
            json.dump(data, json_file)
    with open('anime.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if get:
        return data
    if name not in data:
        data[name] = {
            'animaunt_link': animaunt_link,
            'findanime_link': findanime_link
        }
    with open('anime.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)
    if not get and master:
        master.nametowidget('add_ttl_frame.!entry').delete(0, 'end')
        master.nametowidget('add_ttl_frame.!entry2').delete(0, 'end')
        master.nametowidget('add_ttl_frame.!entry3').delete(0, 'end')
        try:
            master.nametowidget('.uploads_toplvl').destroy()
        except KeyError:
            pass


if __name__ == '__main__':
    pass
