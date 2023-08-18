from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from models import Anime, Dorama
import getpass
import re
import time


USERNAME = getpass.getuser()
CHROME_PATH = (
    f'user-data-dir=C:/Users/{USERNAME}/AppData/Local/Google/Chrome/User Data'
)


def get_options() -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument(CHROME_PATH)
    return options


def parse_animaunt(driver: webdriver.Chrome, episode: Anime) -> None:
    seria = f'{episode.number} серия'
    link_animaunt = episode.animaunt_link
    pattern = r"https://animaunt\.(org|tv)/(\d+)-"
    match = re.search(pattern, link_animaunt)
    id_animaunt = match.group(2)
    driver.get(f'https://animaunt.org/私は独身です.php?mod=editnews&action=editnews&id={id_animaunt}')
    tabplayer1 = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "tabplayer1"))
    )
    divs = tabplayer1.find_elements(By.CLASS_NAME, 'col-sm-12')
    for div in divs:
        input_element = div.find_element(By.TAG_NAME, 'input')
        if input_element.get_attribute('value') == seria:
            code_value = input_element.find_element(
                By.XPATH,
                './following-sibling::input'
            ).get_attribute('value')
            episode.link = code_value
            episode.file = code_value.split('/')[-1]
            break


def parse_malfurik(driver: webdriver.Chrome, episode: Dorama):
    entry_number = episode.number
    url_malf = episode.malfurik_link
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
        if series_title and video_link and f'{entry_number} серия' == series_title.lower():
            found_seria = video_link
            series_info.append({
                'series_title': series_title,
                'video_link': video_link
            })
            episode.link = found_seria
            break


def findanime(driver: webdriver.Chrome, episode: Anime or Dorama, key: str):
    if key == 'anime':
        if not episode.findanime_link:
            return 'Нет на Findanime'
        url = episode.findanime_link
    elif key == 'dorama':
        if not episode.doramatv_link:
            return 'Нет на Doramatv'
        url = episode.doramatv_link
    code_value = episode.link
    entry_number = episode.number
    driver.get(url)
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
                    if match.group(0) == f'Серия {episode_number}':
                        found_episode_link = found_episode_element.get_attribute('href')
                        break
                    else:
                        exclude_number = exclude_number + f' and not(contains(., "{match.group(0)}"))'
                        exclude_list.append(match.group(0))
                        found_episode_element = None
                except Exception:
                    continue

    driver.get(found_episode_link)
    add_video = driver.find_element(By.XPATH, '//a[contains(.,"Добавить видео")]')
    add_video_href = add_video.get_attribute("href")
    driver.get(add_video_href)
    textarea_element = driver.find_element(By.ID, "url")

    if key == 'anime':
        text_to_insert = f'<iframe allowfullscreen="" src="https://animaunt.org/{code_value}" style="border: medium none;" width="100%" height="100%" frameborder="0"></iframe>'
    else:
        text_to_insert = f'<iframe allowfullscreen="" src="https://anime.malfurik.online/play.php?video={code_value}" style="border: medium none;" width="100%" height="100%" frameborder="0"></iframe>'

    textarea_element.send_keys(text_to_insert)
    translation_select = Select(driver.find_element(By.ID, "translationType"))

    if key == 'anime':
        translation_select.select_by_visible_text("Многоголосый")
    else:
        translation_select.select_by_visible_text("Озвучка")

    if key == 'dorama':
        try:
            select_element = driver.find_element(By.CLASS_NAME, "selectize-input.items.not-full.has-options.has-items")
            options = select_element.find_element(By.CLASS_NAME, "item").text
            if "AniMaunt (Переводчик)" in options:
                print('Переводчик указан')
        except Exception as e:
            input_name = driver.find_element(By.CSS_SELECTOR, '.selectize-input.items.not-full.has-options input')
            input_name.send_keys('Animaunt')
            time.sleep(2)  # Время ожидания в секундах, может потребоваться настройка
            input_name.send_keys(Keys.DOWN)
            input_name.send_keys(Keys.ENTER)

    elif key == 'anime':
        div_with_select = driver.find_element(By.XPATH, "//div[select[@placeholder='Начните писать...']]")
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
        driver.execute_script("arguments[0].innerHTML = arguments[1];", div_with_select, new_html)
    time.sleep(1)
    button_post = driver.find_element(By.CLASS_NAME, 'btn-success') #.click()
    button_post.send_keys(Keys.ENTER)
    episode.resilt_link = found_episode_link


def anime365(driver: webdriver.Chrome, anime: Anime, file_path: str):
    if not anime.anime_365_link:
        return 'Нет на Аnime 365'
    if not anime.path:
        return 'Не указан путь к тайтлу'
    entry_number = anime.number
    link_365 = anime.anime_365_link
    driver.get(link_365)
    select_seria = driver.find_element(By.XPATH, f"//a[contains(text(), '{entry_number} серия')]")
    link_seria = select_seria.get_attribute('href')
    driver.get(link_seria)
    link_add = driver.find_elements(By.XPATH, f"//a[contains(text(), 'Добавить перевод')]")[2].get_attribute('href')
    driver.get(link_add)
    select_wrappers = driver.find_elements(By.CLASS_NAME, "select-wrapper")
    select_wrapper = select_wrappers[1]
    actions = webdriver.ActionChains(driver)
    actions.click(select_wrapper).perform()
    voice_option = driver.find_element(By.XPATH, "//li[contains(., 'Озвучка')]")
    voice_option.click()
    authors_input = driver.find_element(By.ID, 'TranslationAdminForm_authorsNew')
    authors_input.send_keys('Animaunt')
    file_input = driver.find_element(By.NAME, 'qqfile')
    file_input.send_keys(file_path)
    wait = WebDriverWait(driver, 10000)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "qq-upload-success")))
    add_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Добавить перевод')]")
    add_btn.click()
    WebDriverWait(driver, 100).until(EC.url_changes(link_add))
    card_div = driver.find_element(By.CLASS_NAME, 'card-content')
    upload_link_365 = card_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
    return upload_link_365


if __name__ == '__main__':
    pass