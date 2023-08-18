from data import update_or_get_data, path_choice
from selenium import webdriver
from parse import get_options, findanime, anime365
from searchfolder import find_file
import tkinter as tk
import ttkbootstrap as tb
from models import Anime, Dorama
from parse import parse_animaunt, parse_malfurik
from typing import List


def upload(master: tk.Tk, uploads: str, key: str):
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
    episodes = analyze(master, uploads, key)
    options = get_options()
    pb = master.nametowidget('links_list_frame.pb')
    pb.config(maximum=(len(episodes)))
    text = master.nametowidget('links_list_frame.findanime_links')
    try:
        for episode in episodes:
            if key == 'anime':
                driver = webdriver.Chrome(options=options)
                driver.minimize_window()
                parse_animaunt(driver, episode)
                pb.step(1)
            elif key == 'dorama':
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
                parse_malfurik(driver, episode)
                pb.step(1)
        pb['value'] = 0
        driver.close()
        options = get_options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        for episode in episodes:
            findanime(driver, episode, key)
            text.config(state=tk.NORMAL)
            text.insert(tk.END, f'{episode.resilt_link}\n')
            text.config(state=tk.DISABLED)
            pb.step(1)
        pb['value'] = 0
        if key != 'dorama':
            text = master.nametowidget('links_list_frame.anime_365_links')
            for episode in episodes:
                file_path = find_file(episode.path, episode.file)
                link = anime365(driver, episode, file_path)
                text.config(state=tk.NORMAL)
                text.insert(tk.END, f'{link}\n')
                text.config(state=tk.DISABLED)
                pb.step(1)
        pb['value'] = 0
        upload_bttn.config(state=tk.NORMAL)
        driver.close()
    except Exception as e:
        upload_bttn.config(state=tk.NORMAL)
        driver.close()
        print(e)


def uploads_toplvl(
        master: tk.Tk,
        episode: Anime or Dorama,
        key: str,
        ):
    uplds = tk.Toplevel(master, name='uploads_toplvl')
    uplds.title('Uploads Data')
    uplds.geometry('392x400+400+100')
    uplds.resizable(False, False)

    title_name_lbl = tb.Label(
        uplds,
        text=f'Добавьте ссылки для {episode.name}',
        wraplength=280,
    )
    title_name_lbl.grid(column=0, row=0, pady=6, padx=6, sticky='n')

    if key == 'anime':
        animaunt_link_name_lbl = tb.Label(uplds, text='Ссылка на Animaunt')
        animaunt_link_name_lbl.grid(column=0, row=1, pady=6, padx=6, sticky='n')

        animaunt_link_entry = tb.Entry(uplds, width=60)
        animaunt_link_entry.grid(column=0, row=2, pady=6, padx=8)

        findanime_link_name_lbl = tb.Label(uplds, text='Ссылка на Findanime')
        findanime_link_name_lbl.grid(column=0, row=3, pady=6, padx=6, sticky='n')

        findanime_link_entry = tb.Entry(uplds, width=60)
        findanime_link_entry.grid(column=0, row=4, pady=6, padx=8)

        anime_365_link_name_lbl = tb.Label(uplds, text='Ссылка на Аnime 365')
        anime_365_link_name_lbl.grid(column=0, row=5, pady=6, padx=6, sticky='n')

        anime_365_link_entry = tb.Entry(uplds, width=60)
        anime_365_link_entry.grid(column=0, row=6, pady=6, padx=8)

        add_folder_lbl = tb.Label(uplds, text='Путь к папке с аниме')
        add_folder_lbl.grid(column=0, row=7, pady=6, padx=6, sticky='n')

        add_folder_bttn = tb.Button(
            uplds,
            width=18,
            name='add_folder_bttn',
            text='Выбрать папку',
        )
        add_folder_bttn.grid(column=0, row=8, pady=5, padx=5)
        add_folder_bttn.config(
            command=lambda: path_choice(episode.name, master, add_folder_bttn)
        )

        add_ttl_bttn = tb.Button(
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

    elif key == 'dorama':
        malfurik_link_name_lbl = tb.Label(uplds, text='Ссылка на Malfurik')
        malfurik_link_name_lbl.grid(column=0, row=1, pady=6, padx=6, sticky='n')

        malfurik_link_entry = tb.Entry(uplds, width=60)
        malfurik_link_entry.grid(column=0, row=2, pady=6, padx=8)

        doramatv_link_name_lbl = tb.Label(uplds, text='Ссылка на Doramatv')
        doramatv_link_name_lbl.grid(column=0, row=3, pady=6, padx=6, sticky='n')

        doramatv_link_entry = tb.Entry(uplds, width=60)
        doramatv_link_entry.grid(column=0, row=4, pady=6, padx=8)

        add_ttl_bttn = tb.Button(
            uplds,
            text='Добавить тайтл',
            width=18,
            command=lambda: update_or_get_data(
                episode.name,
                malfurik_link_entry.get().strip(),
                doramatv_link_entry.get().strip(),
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


def analyze(master: tk.Tk, uploads: str, key: str) -> List[Anime or Dorama]:
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
                                epsd.malfurik_link = data[epsd.name]['malfurik_link']
                                flag = True
                            except KeyError:
                                pass
                episodes.append(epsd)
        return episodes
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pass
