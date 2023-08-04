import configparser


def write_config(key: str, value: str) -> None:
    config = get_config()
    config['PATHS'][key] = value
    with open('AnimauntUploader.ini', 'w', encoding='utf-8') as config_file:
        config.write(config_file)


def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('AnimauntUploader.ini', encoding='utf-8')
    if 'PATHS' not in config:
        config['PATHS'] = {}
    return config


if __name__ == '__main__':
    pass
