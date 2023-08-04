import os
import re

def clean_text(text):
    cleaned_text = re.sub(r'[?!:—,.]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip().lower()
    return cleaned_text

def find_single_folder(root_folder, target_text):
    cleaned_target = clean_text(target_text)
    words = cleaned_target.split()
    current_search = words[0]

    while True:
        matching_folders = []
        for root, dirs, files in os.walk(root_folder):
            for dir_name in dirs:
                cleaned_dir_name = clean_text(dir_name)
                if current_search in cleaned_dir_name:
                    matching_folders.append(os.path.join(root, dir_name))
        
        if len(matching_folders) == 1:
            return matching_folders[0]
        
        if not matching_folders:
            return None
        
        current_search = ' '.join(words[:len(current_search.split()) + 1])

def find_file(found_folder, target_name_video):
    for root, dirs, files in os.walk(found_folder):
        if target_name_video in files:
            return os.path.join(root, target_name_video)
    
    return None


# root_folder = "Z:\Animaunt\Anime" # основной путь.
# target_text = "Девушка на час" # тут имя с БД или Введенное которое.
# target_name_video = '04x.mp4' # тут имя файла, скопированное с ссылки взятое в анимают.

# found_folder = find_single_folder(root_folder, target_text)
# if found_folder:
#     print(found_folder)
# else:
#     print("Папка не найдена.")


# found_file = find_file(found_folder, target_name_video)
# if found_file:
#     print(found_file)
# else:
#     print("Файл не найден.")

if __name__ == '__main__':
    pass
