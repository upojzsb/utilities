# Written by upojzsb
# Version 1.0 is released on March 4, 2021
# This software is released under Apache License 2.0
# The license is shown in LICENSE file.

import re
# import json
import requests

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
headers = {
    'User-Agent': user_agent
}


def get_song_url_in_page(page_url):
    """
    :param page_url: Page_url
    :return: [(title, url), ...]
    """
    base_url = 'https://www.ximalaya.com'
    audio_lookup_base_url = 'https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1' # song_number

    proxies = {
        "http": None,
        "https": None,
    }

    # Find music lists
    pattern1 = re.compile('<div class="sound-list _is"><ul>(.*)</ul><div class="pagination _is">')
    # Find url
    pattern2 = re.compile('<a title="(.*)" href="(.*?)">')

    r = requests.get(url=page_url, proxies=proxies, headers=headers)
    contents = str(r.content)
    contents = pattern1.findall(contents)[0].split('<li class="lF_">')[1:]

    songs_url = []
    for content in contents:
        song = pattern2.findall(content)[0]

        song_title, song_number = song
        song_number = song_number[song_number.rfind('/')+1:]

        song_url_getter_url = audio_lookup_base_url % song_number
        r = requests.get(url=song_url_getter_url, proxies=proxies, headers=headers)

        song_url = r.json()['data']['src']

        songs_url.append((song_title, song_url))

    return songs_url


def main():
    base_playlist_page = input('Enter baseurl (such as https://www.ximalaya.com/waiyu/9899064/): ') + 'p%d/'
    start = int(input('Enter start page (such as 1): '))
    end = int(input('Enter end page (such as 8): '))
    pages = [base_playlist_page % page for page in range(start, end + 1)]

    print('Songs\' list in in ', pages, 'will be download.')

    song_list = []

    for page in pages:
        song_list += get_song_url_in_page(page)

    for song in song_list:
        print(song[1])# , song[0]+song[1][song[1].rfind('.'):])


if __name__ == '__main__':
    main()
