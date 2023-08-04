def anime365():
    entry_number = entry.get()
    # ссылка на 365
    link_365 = 'https://anime365.ru/catalog/eiyuu-kyoushitsu-25601'
    driver.get(link_365)
    select_seria = driver.find_element(By.XPATH, f"//a[contains(text(), '{entry_number} серия')]")
    link_seria = select_seria.get_attribute('href')
    driver.get(link_seria)
    link_add = driver.find_elements(By.XPATH, f"//a[contains(text(), 'Добавить перевод')]")[2].get_attribute('href')
    driver.get(link_add)


    select_wrappers = driver.find_elements(By.CLASS_NAME, "select-wrapper")
    select_wrapper = select_wrappers[1]
    actions = ActionChains(driver)
    actions.click(select_wrapper).perform()
    voice_option = driver.find_element(By.XPATH, "//li[contains(., 'Озвучка')]")
    voice_option.click()
    authors_input = driver.find_element(By.ID, 'TranslationAdminForm_authorsNew')
    authors_input.send_keys('Animaunt')

    # Загрузка файла
    file_input = driver.find_element(By.NAME, 'qqfile')
    file_path = 'D:\YandexDisk\Загрузки\Аниме\Ублюдок/26x.mp4' #тут путь загрузки файла
    file_input.send_keys(file_path)

    wait = WebDriverWait(driver, 10000)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "qq-upload-success")))
    add_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Добавить перевод')]")
    add_btn.click()
    card_div = driver.find_element(By.CLASS_NAME, 'card-content')
    upload_link_365 = card_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
    return upload_link_365