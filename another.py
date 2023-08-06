def post_malf():
    entry_number = entry.get()  # номер серии
    url_malf = 'https://anime.malfurik.online/movie/nakazanie/'  # ссылка малф
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

    print(found_seria)  # это ссылка на видео