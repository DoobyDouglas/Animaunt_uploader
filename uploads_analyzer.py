from data import update_or_get_data, path_choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from slnm import get_options, findanime, anime365
from searchfolder import find_file
import tkinter as tk
import ttkbootstrap as ttk
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


class Dorama:
    def __init__(
            self,
            name,
            number,
            malfurik_link=None,
            ) -> None:
        self.name = name
        self.number = number
        self.malfurik_link = malfurik_link
        self.doramatv_link = None
        self.link = None

    def __str__(self) -> str:
        return self.name

    def get_link(self):
        options = get_options()
        entry_number = self.number
        url_malf = self.malfurik_link
        driver = webdriver.Chrome(options=options)
        driver.get(url_malf)
        edit_li = driver.find_element(By.ID, 'wp-admin-bar-edit')
        edit_link = edit_li.find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(edit_link)
        series_elements = driver.find_elements(By.CLASS_NAME, 'rwmb-group-clone')
        series_info = []
        for series_element in series_elements:
            title_element = series_element.find_element(By.CLASS_NAME, 'rwmb-text')
            series_title = title_element.get_attribute('value')
            video_elemment = series_element.find_elements(By.TAG_NAME, 'input')[1]
            video_link = video_elemment.get_attribute('value')
            if series_title and video_link and entry_number in series_title:
                found_seria = video_link
                series_info.append({
                    'series_title': series_title,
                    'video_link': video_link
                })
                self.link = found_seria
                return


def uploads_toplvl(
        master: tk.Tk,
        episode: Anime or Dorama,
        key: str,
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
            key=key,
        ),
    )
    add_ttl_bttn.grid(column=0, row=9, pady=12, padx=10)

    uplds.wm_attributes('-topmost', 1)
    uplds.wm_attributes('-topmost', 0)
    uplds.grab_set()
    uplds.focus_force()
    uplds.wait_window()


def uploads_analyze(uploads: str, master: tk.Tk, key: str):
    upload_bttn = master.nametowidget('upload_list_frame.upload_bttn')
    upload_bttn.config(state=tk.DISABLED)
    txt_widget_names = [
        'links_list_frame.findanime_links',
        'links_list_frame.anime_365_links'
    ]
    for widget_name in txt_widget_names:
        text = master.nametowidget(widget_name)
        text.config(state=tk.NORMAL)
        text.delete('1.0', tk.END)
        text.config(state=tk.DISABLED)
    episodes = []
    data = update_or_get_data(get=True)

    try:
        for line in uploads.splitlines():
            number = line.split()[-1]
            if number.isdigit():
                name = ' '.join(line.split()[:-1])
                if key == 'anime':
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
                            uploads_toplvl(master, epsd, key)
                            data = update_or_get_data(get=True)
                            try:
                                epsd.animaunt_link = data[epsd.name]['animaunt_link']
                                flag = True
                            except KeyError:
                                pass
                elif key == 'dorama':
                    epsd = Dorama(name, number)
                    flag = False
                    if epsd.name in data:
                        epsd.malfurik_link = data[epsd.name]['malfurik_link']
                        epsd.doramatv_link = data[epsd.name]['doramatv_link']
                        flag = True
                    else:
                        while not flag:
                            uploads_toplvl(master, epsd, key)
                            data = update_or_get_data(get=True)
                            try:
                                epsd.malfurik_ = data[epsd.name]['malfurik_link']
                                flag = True
                            except KeyError:
                                pass
                episodes.append(epsd)
        pb = master.nametowidget('links_list_frame.pb')
        pb.config(maximum=(len(episodes) * 2))
        for episode in episodes:
            episode.get_link()
        text = master.nametowidget('links_list_frame.findanime_links')
        for episode in episodes:
            link = findanime(episode, key)
            text.config(state=tk.NORMAL)
            text.insert(tk.END, f'{link}\n')
            text.config(state=tk.DISABLED)
            pb.step(1)
        text = master.nametowidget('links_list_frame.anime_365_links')
        if key != 'dorama':
            for anime in episodes:
                if anime.path:
                    file_path = find_file(anime.path, anime.file)
                    link = anime365(anime, file_path)
                    text.config(state=tk.NORMAL)
                    text.insert(tk.END, f'{link}\n')
                else:
                    text.config(state=tk.NORMAL)
                    text.insert(tk.END, 'Не указан путь к тайтлу\n')
                text.config(state=tk.DISABLED)
                pb.step(1)
        upload_bttn.config(state=tk.NORMAL)
        pb['value'] = 0
    except Exception:
        upload_bttn.config(state=tk.NORMAL)


if __name__ == '__main__':
    pass
