import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re
import time

USERNAME = getpass.getuser()
CHROME_PATH = (
    f'user-data-dir=C:/Users/{USERNAME}/AppData/Local/Google/Chrome/User Data'
)


def get_options():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument(CHROME_PATH)
    return options


def found():
    found_episode_element = None
    exclude_list = []
    exclude_number = 'and not(contains(., "Серия 10000"))'
    while not found_episode_element:
        for i in range(1, 20):
            if i not in exclude_list:
                try:
                    episode_number = entry_number
                    episode_xpath = f'//a[contains(.,"Серия {episode_number}") {exclude_number}]'
                    found_episode_element = driver.find_element(By.XPATH, episode_xpath)
                    found_episode_text = found_episode_element.get_attribute('text')
                    match = re.search(r'Серия (\d+)', found_episode_text)
                    m = match.group(0)
                    if match.group(0) == f'Серия {episode_number}':
                        found_episode_link = found_episode_element.get_attribute('href')
                        print(found_episode_link)
                        break
                    else:
                        exclude_number = exclude_number + f' and not(contains(., "{match.group(0)}"))'
                        exclude_list.append(match.group(0))
                        found_episode_element = None
                except Exception:
                    continue


def findanime(anime):
    code_value = anime.get_link()
    options = get_options()
    entry_number = anime.number
    url = anime.findanime_link
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    found_episode_element = driver.find_element(By.XPATH, f'//a[contains(.,"Серия {entry_number}")]')
    found_episode_link = found_episode_element.get_attribute('href')
    print(found_episode_link)
    driver.get(found_episode_link)
    add_video = driver.find_element(By.XPATH, '//a[contains(.,"Добавить видео")]')
    add_video_href = add_video.get_attribute("href")
    print(add_video_href)
    driver.get(add_video_href)
    textarea_element = driver.find_element(By.ID, "url")
    # тут нужно поменять на ссылку, стандарт + ссылка которую получили
    # <iframe allowfullscreen="" src = "https://animaunt.org/{code_value}" style="border: medium none;" width="100%" height="100%" frameborder="0"></iframe>
    # типа вот такой код и там code_value, вроде я правильно ее написал
    text_to_insert = f'<iframe allowfullscreen="" src = "https://animaunt.org/{code_value}" style="border: medium none;" width="100%" height="100%" frameborder="0"></iframe>'

    textarea_element.send_keys(text_to_insert)
    translation_select = Select(driver.find_element(By.ID, "translationType"))
    translation_select.select_by_visible_text("Многоголосый")

    div_with_select = driver.find_element(By.XPATH, "//div[select[@placeholder='Начните писать...']]")

    # Новый HTML-код, который вы хотите вставить
    new_html = """
        <select name="personAndType" class="select-role-null form-control selectized" multiple="multiple" placeholder="Начните писать..." style="display: none;" tabindex="-1">
            <option value="7035:4" selected="selected">AniMaunt</option>
        </select>
        <div class="selectize-control select-role-null form-control multi plugin-remove_button">
            <div class="selectize-input items not-full has-options has-items">
                <div class="item active" data-value="7035:4">AniMaunt <span class="label label-info">Переводчик</span>
                    <a href="javascript:void(0)" class="remove" tabindex="-1" title="Remove">×</a>
                </div>
                <input type="select-multiple" autocomplete="off" autofill="no" tabindex="" style="width: 4px; opacity: 1; position: relative; left: 0px;">
            </div>
            <div class="selectize-dropdown multi select-role-null form-control plugin-remove_button" style="display: none; visibility: visible; width: 326.656px; top: 40.9844px; left: 0px;">
                <div class="selectize-dropdown-content" tabindex="-1"></div>
            </div>
        </div>
        <script type="text/javascript">
            $(function (){
                rm_h.addAjaxSelectize('.select-role-null', {
                    ajaxUrl: '/search/personsRoles?forChapter=true',
                    maxItems: 2
                });
            })
        </script>
    """

    # Заменяем содержимое элемента новым HTML-кодом с помощью JavaScript
    driver.execute_script("arguments[0].innerHTML = arguments[1];", div_with_select, new_html)

    # надо добавить будет клик на пост стр, и выводить ссылку в программу, когда он запостил found_episode_link вот эту.
    driver.quit()


if __name__ == '__main__':
    pass
