from data import update_or_get_data
from selenium import webdriver
from selenium.webdriver.common.by import By
from slnm import get_options, findanime
import tkinter
import ttkbootstrap as ttk


class Anime:
    def __init__(
            self,
            name,
            number,
            animaunt_link=None,
            findanime_link=None,
            ) -> None:
        self.name = name
        self.number = number
        self.animaunt_link = animaunt_link
        self.findanime_link = findanime_link

    def __str__(self) -> str:
        return self.name

    def get_link(self) -> str:
        options = get_options()
        seria = f'{self.number} серия'
        driver = webdriver.Chrome(options=options)
        driver.get(self.animaunt_link)
        tabplayer1 = driver.find_element(By.ID, "tabplayer1")
        divs = tabplayer1.find_elements(By.CLASS_NAME, 'col-sm-12')
        for div in divs:
            input_element = div.find_element(By.TAG_NAME, 'input')
            if input_element.get_attribute('value') == seria:
                code_value = input_element.find_element(
                    By.XPATH,
                    './following-sibling::input'
                ).get_attribute('value')
                return code_value


def uploads_toplvl(
        master: tkinter.Tk,
        episode: Anime,
        ):
    uplds = tkinter.Toplevel(master, name='uploads_toplvl')
    uplds.title('Uploads Data')
    uplds.geometry('392x230')
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

    add_ttl_bttn = ttk.Button(
        uplds,
        text='Добавить ссылки',
        width=18,
        command=lambda: update_or_get_data(
            episode.name,
            animaunt_link_entry.get().strip(),
            findanime_link_entry.get().strip(),
            master=master,
        ),
    )
    add_ttl_bttn.grid(column=0, row=5, pady=12, padx=10)

    uplds.focus_force()
    uplds.wait_window()


def uploads_analyze(uploads: str, master: tkinter.Tk):
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
                flag = True
            else:
                uploads_toplvl(master, epsd)
                data = update_or_get_data(get=True)
                try:
                    epsd.animaunt_link = data[epsd.name]['animaunt_link']
                    epsd.findanime_link = data[epsd.name]['findanime_link']
                    flag = True
                except KeyError:
                    pass
            if flag:
                anime_list.append(epsd)
    for anime in anime_list:
        # link = findanime(anime)
        link = 'Тут ссылка из функции "findanime"'
        text = master.nametowidget('links_list_frame.!text')
        text.config(state='normal')
        text.insert(tkinter.END, f'{link}\n')
        text.config(state='normal')
        text.config(state='disabled')


if __name__ == '__main__':
    pass
