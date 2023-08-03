from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter
from ttkbootstrap import Style
import ttkbootstrap as ttk
from data import update_or_get_data
from uploads_analyzer import uploads_analyze

NAME = 'Findanime Uploader'
VERSION = 0.01

master = tkinter.Tk()
master.title(f'{NAME} v{VERSION:.2f}')
master.geometry('865x500')
master.resizable(False, False)

style = Style(theme='superhero')

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

add_ttl_bttn = ttk.Button(
    add_ttl_frame,
    text='Добавить тайтл',
    width=18,
    command=lambda: update_or_get_data(
        ttl_name_entry.get().strip(),
        animaunt_link_entry.get().strip(),
        findanime_link_entry.get().strip(),
        master=master,
    ),
)
add_ttl_bttn.grid(column=0, row=6, pady=10, padx=5)

upload_list_frame = ttk.Frame(master, name='upload_list_frame')
upload_list_frame.pack(side='left', anchor='ne', padx=15, pady=10)

upload_list_lbl = ttk.Label(upload_list_frame, text='Список заливок')
upload_list_lbl.grid(column=0, row=0, pady=5, padx=5, sticky='w')

uploads = ttk.Text(upload_list_frame, width=50, wrap='none')
uploads.grid(column=0, row=1, pady=5, padx=5)

upload_bttn = ttk.Button(
    upload_list_frame,
    text='Залить тайтлы',
    width=20,
    command=lambda: uploads_analyze(
        uploads.get('1.0', 'end'),
        master,
    ),
)
upload_bttn.grid(column=0, row=2, pady=10, padx=5, sticky='se')

links_list_frame = ttk.Frame(master, name='links_list_frame')
links_list_frame.pack(side='left', anchor='ne', padx=10, pady=10)

links_list_lbl = ttk.Label(links_list_frame, text='Список загрузок')
links_list_lbl.grid(column=0, row=0, pady=5, padx=5, sticky='w')

links = ttk.Text(links_list_frame, width=50, wrap='none', state='disabled')
links.grid(column=0, row=1, pady=5, padx=5)


if __name__ == '__main__':
    master.mainloop()
