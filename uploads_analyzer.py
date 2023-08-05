from data import update_or_get_data, path_choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from slnm import get_options, findanime, anime365
from config import get_config
from searchfolder import find_single_folder, find_file
import tkinter as tk
import ttkbootstrap as ttk
import os
import time
import re


class Anime:
    def __init__(
            self,
            name,
            number,
            animaunt_link=None,
            findanime_link=None,
            anime_365_link=None,
            path=None,
            ) -> None:
        self.name = name
        self.number = number
        self.animaunt_link = animaunt_link
        self.findanime_link = findanime_link
        self.anime_365_link = anime_365_link
        self.path = path
        self.link = None
        self.file = None

    def __str__(self) -> str:
        return self.name

    def get_link(self) -> str:
        options = get_options()
        seria = f'{self.number} серия'
        driver = webdriver.Chrome(options=options)
        link_animaunt = self.animaunt_link
        pattern = r"https://animaunt\.(org|tv)/(\d+)-"
        match = re.search(pattern, link_animaunt)
        id_animaunt = match.group(2)
        driver.get(f'https://animaunt.org/私は独身です.php?mod=editnews&action=editnews&id={id_animaunt}')
        tabplayer1 = driver.find_element(By.ID, "tabplayer1")
        divs = tabplayer1.find_elements(By.CLASS_NAME, 'col-sm-12')
        for div in divs:
            input_element = div.find_element(By.TAG_NAME, 'input')
            if input_element.get_attribute('value') == seria:
                code_value = input_element.find_element(
                    By.XPATH,
                    './following-sibling::input'
                ).get_attribute('value')
                self.link = code_value
                self.file = code_value.split('/')[-1]
                return


def uploads_toplvl(
        master: tk.Tk,
        episode: Anime,
        ):
    uplds = tk.Toplevel(master, name='uploads_toplvl')
    uplds.title('Uploads Data')
    uplds.geometry('392x400+400+100')
    uplds.resizable(False, False)

    title_name_lbl = ttk.Label(
        uplds,
        text=f'Добавьте ссылки для {episode.name}',
        wraplength=280,
    )
    title_name_lbl.grid(column=0, row=0, pady=6, padx=6, sticky='n')

    animaunt_link_name_lbl = ttk.Label(uplds, text='Ссылка на Animaunt')
    animaunt_link_name_lbl.grid(column=0, row=1, pady=6, padx=6, sticky='n')

    animaunt_link_entry = ttk.Entry(uplds, width=60)
    animaunt_link_entry.grid(column=0, row=2, pady=6, padx=8)

    findanime_link_name_lbl = ttk.Label(uplds, text='Ссылка на Findanime')
    findanime_link_name_lbl.grid(column=0, row=3, pady=6, padx=6, sticky='n')

    findanime_link_entry = ttk.Entry(uplds, width=60)
    findanime_link_entry.grid(column=0, row=4, pady=6, padx=8)

    anime_365_link_name_lbl = ttk.Label(uplds, text='Ссылка на Аnime 365')
    anime_365_link_name_lbl.grid(column=0, row=5, pady=6, padx=6, sticky='n')

    anime_365_link_entry = ttk.Entry(uplds, width=60)
    anime_365_link_entry.grid(column=0, row=6, pady=6, padx=8)

    add_folder_lbl = ttk.Label(uplds, text='Путь к папке с аниме')
    add_folder_lbl.grid(column=0, row=7, pady=6, padx=6, sticky='n')

    add_folder_bttn = ttk.Button(
            uplds,
            width=18,
            name='add_folder_bttn',
            text='Выбрать папку',
        )
    add_folder_bttn.grid(column=0, row=8, pady=5, padx=5)
    add_folder_bttn.config(
        command=lambda: path_choice(episode.name, master, add_folder_bttn)
    )

    add_ttl_bttn = ttk.Button(
        uplds,
        text='Добавить тайтл',
        width=18,
        command=lambda: update_or_get_data(
            episode.name,
            animaunt_link_entry.get().strip(),
            findanime_link_entry.get().strip(),
            anime_365_link_entry.get().strip(),
            master=master,
        ),
    )
    add_ttl_bttn.grid(column=0, row=9, pady=12, padx=10)

    uplds.wm_attributes('-topmost', 1)
    uplds.wm_attributes('-topmost', 0)
    uplds.grab_set()
    uplds.focus_force()
    uplds.wait_window()


def uploads_analyze(uploads: str, master: tk.Tk):
    upload_bttn = master.nametowidget('upload_list_frame.upload_bttn')
    upload_bttn.config(state=tk.DISABLED)
    anime_list = []
    data = update_or_get_data(get=True)
    for line in uploads.splitlines():
        number = line.split()[-1]
        if number.isdigit():
            name = ' '.join(line.split()[:-1])
            epsd = Anime(name, number)
            flag = False
            if epsd.name in data:
                epsd.animaunt_link = data[epsd.name]['animaunt_link']
                epsd.findanime_link = data[epsd.name]['findanime_link']
                epsd.anime_365_link = data[epsd.name]['anime_365_link']
                epsd.path = data[epsd.name]['path']
                flag = True
            else:
                while not flag:
                    uploads_toplvl(master, epsd)
                    data = update_or_get_data(get=True)
                    try:
                        epsd.animaunt_link = data[epsd.name]['animaunt_link']
                        epsd.findanime_link = data[epsd.name]['findanime_link']
                        epsd.anime_365_link = data[epsd.name]['anime_365_link']
                        epsd.path = data[epsd.name]['path']
                        flag = True
                    except KeyError:
                        pass
            anime_list.append(epsd)
    pb = master.nametowidget('links_list_frame.pb')
    pb.config(maximum=(len(anime_list) * 2))
    for anime in anime_list:
        anime.get_link()
        # print(anime.name)
        # print(anime.animaunt_link)
        # print(anime.findanime_link)
        # print(anime.anime_365_link)
        # print(anime.path)
        # print(anime.file)
        # print(anime.link)
    for anime in anime_list:
        link = findanime(anime)
        text = master.nametowidget('links_list_frame.findanime_links')
        text.config(state=tk.NORMAL)
        text.insert(tk.END, f'{link}\n')
        text.config(state=tk.DISABLED)
        pb.step(1)
    # flag = False
    # while not flag:
    #     try:
    #         config = get_config()
    #         if config['PATHS']['anime_path'] != '':
    #             folder = config['PATHS']['anime_path']
    #             flag = True
    #         else:
    #             path_choice(master)
    #     except KeyError:
    #         path_choice(master)
    for anime in anime_list:
        # found_folder = find_single_folder(folder, anime.name)
        if anime.path and anime.file:
            file_path = find_file(anime.path, anime.file)
            link = anime365(anime, file_path)
            text = master.nametowidget('links_list_frame.anime_365_links')
            text.config(state=tk.NORMAL)
            text.insert(tk.END, f'{link}\n')
        else:
            text.config(state=tk.NORMAL)
            text.insert(tk.END, 'Нет пути или файла\n')
        text.config(state=tk.DISABLED)
        pb.step(1)
    upload_bttn.config(state=tk.NORMAL)
    pb['value'] = 0


if __name__ == '__main__':
    pass