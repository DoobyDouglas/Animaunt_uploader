# pyinstaller --noconfirm --onefile AnimauntUploader.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from ttkbootstrap import Style
import ttkbootstrap as ttk
from data import update_or_get_data, path_choice
from uploads_analyzer import uploads_analyze
from threading import Thread
from config import get_config


NAME = 'AnimauntUploader'
VERSION = 0.06


def on_upload_bttn(
        uploads: str,
        master: tk.Tk,
        ):
    thread = Thread(target=uploads_analyze, args=(uploads, master))
    thread.start()


config = get_config()

master = tk.Tk()
master.title(f'{NAME} v{VERSION:.2f}')
master.geometry('1215x478+500+150')
master.resizable(False, False)

style = Style(theme='superhero')
style.configure('Horizontal.TProgressbar', thickness=25)

add_ttl_frame = ttk.Frame(master, name='add_ttl_frame')
add_ttl_frame.pack(side='left', anchor='nw', padx=10, pady=10)

ttl_name_lbl = ttk.Label(add_ttl_frame, text='Название')
ttl_name_lbl.grid(column=0, row=0, pady=5, padx=5, sticky='w')

ttl_name_entry = ttk.Entry(add_ttl_frame)
ttl_name_entry.grid(column=0, row=1, pady=5, padx=5)

animaunt_link_name_lbl = ttk.Label(add_ttl_frame, text='Ссылка на Animaunt')
animaunt_link_name_lbl.grid(column=0, row=2, pady=5, padx=5, sticky='w')

animaunt_link_entry = ttk.Entry(add_ttl_frame)
animaunt_link_entry.grid(column=0, row=3, pady=5, padx=5)

findanime_link_name_lbl = ttk.Label(add_ttl_frame, text='Ссылка на Findanime')
findanime_link_name_lbl.grid(column=0, row=4, pady=5, padx=5, sticky='w')

findanime_link_entry = ttk.Entry(add_ttl_frame)
findanime_link_entry.grid(column=0, row=5, pady=5, padx=5)

anime_365_link_name_lbl = ttk.Label(add_ttl_frame, text='Ссылка на Аnime 365')
anime_365_link_name_lbl.grid(column=0, row=6, pady=5, padx=5, sticky='w')

anime_365_link_entry = ttk.Entry(add_ttl_frame)
anime_365_link_entry.grid(column=0, row=7, pady=5, padx=5)

add_folder_lbl = ttk.Label(add_ttl_frame, text='Путь к папке с аниме')
add_folder_lbl.grid(column=0, row=8, pady=5, padx=5, sticky='w')


add_folder_bttn = ttk.Button(
    add_ttl_frame,
    width=18,
    name='add_folder_bttn',
    command=lambda: path_choice(ttl_name_entry.get().strip(), master),
    text='Выбрать папку'
)
add_folder_bttn.grid(column=0, row=9, pady=5, padx=5)

add_ttl_bttn = ttk.Button(
    add_ttl_frame,
    text='Добавить тайтл',
    width=18,
    command=lambda: update_or_get_data(
        ttl_name_entry.get().strip(),
        animaunt_link_entry.get().strip(),
        findanime_link_entry.get().strip(),
        anime_365_link_entry.get().strip(),
        master=master,
    ),
)
add_ttl_bttn.grid(column=0, row=10, pady=38, padx=5)

# add_folder_frame = ttk.Frame(master, name='add_folder_frame')
# add_folder_frame.place(anchor='nw', y=355, x=10)



upload_list_frame = ttk.Frame(master, name='upload_list_frame')
upload_list_frame.pack(side='left', anchor='ne', padx=15, pady=10)

upload_list_lbl = ttk.Label(upload_list_frame, text='Список заливок')
upload_list_lbl.grid(column=0, row=0, pady=5, padx=5, sticky='w')

uploads = ttk.Text(upload_list_frame, width=50, wrap='none')
uploads.grid(column=0, row=1, pady=5, padx=5)

upload_bttn = ttk.Button(
    upload_list_frame,
    text='Залить тайтлы',
    name='upload_bttn',
    width=20,
    command=lambda: on_upload_bttn(
        uploads.get('1.0', 'end'),
        master,
    ),
)
upload_bttn.grid(column=0, row=2, pady=10, padx=5, sticky='se')

links_list_frame = ttk.Frame(master, name='links_list_frame')
links_list_frame.pack(side='left', anchor='ne', padx=10, pady=10)

findanime_list_lbl = ttk.Label(
    links_list_frame,
    text='Список загрузок на Findanime',
)
findanime_list_lbl.grid(column=0, row=0, pady=5, padx=5, sticky='w')

findanime_links = ttk.Text(
    links_list_frame,
    width=50,
    name='findanime_links',
    wrap='none',
    state=tk.DISABLED,
)
findanime_links.grid(column=0, row=1, pady=5, padx=5)

pb = ttk.Progressbar(
    links_list_frame,
    mode='determinate',
    name='pb',
    length=664,
)
pb.grid(column=0, row=2, pady=10, padx=5, sticky='w', columnspan=2)

anime_365_list_lbl = ttk.Label(
    links_list_frame,
    text='Список загрузок на Аnime 365',
)
anime_365_list_lbl.grid(column=1, row=0, pady=5, padx=30, sticky='w')

anime_365_links = ttk.Text(
    links_list_frame,
    width=50,
    name='anime_365_links',
    wrap='none',
    state=tk.DISABLED,
)
anime_365_links.grid(column=1, row=1, pady=5, padx=30)


if __name__ == '__main__':
    master.mainloop()
