import requests
import os
import argparse
from dotenv import load_dotenv


def cut_link(token, original_url):
    params = {
        'v': '5.199',
        'access_token': token,
        'url': original_url,
        'private': 0
    }
    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
    response.raise_for_status()
    short_url = response.json()
    return short_url['response']['short_url']


def count_clicks(token, url_key):
    params = {
        'v': '5.199',
        'access_token': token,
        'key': url_key,
        'interval': 'forever',
        'interval_counts': 'forever',
        'extended': 1
    }
    response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=params)
    response.raise_for_status()
    counted_clicks = response.json()
    return counted_clicks['response']['stats'][0]['views']


def is_shorted_link(token, url_to_check):
    params = {
        'v': '5.199',
        'access_token': token,
        'url': url_to_check,
        'private': 0
    }
    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
    response.raise_for_status()
    short_url = response.json()
    return 'error' not in short_url


def main():
    try:
        load_dotenv()
        token = os.environ['VK_TOKEN']
        parser = argparse.ArgumentParser(description='Программа для работы с вк ссылками')
        parser.add_argument('link', help='вставьте ссылку')
        args = parser.parse_args()
        user_link = args.link

        if 'vk.cc/' in user_link:
            url_key = user_link.split('vk.cc/')[-1]
            clicks = count_clicks(token, url_key)
            print(f'По ссылке перешло: {clicks}')
        else:
            short_url = cut_link(token, user_link)
            print(f'Короткая ссылка: {short_url}')

    except requests.exceptions.HTTPError:
        print('Ошибка соединения')
    except KeyError:
        print('Ошибка: VK_TOKEN не найден')


if __name__ == '__main__':
    main()

