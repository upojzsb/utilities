import requests
import tkinter as tk
import io
from PIL import Image, ImageTk
import time


def _read_config(path=None):
    if path is None:
        path = 'msc_config.txt'

    with open(path, 'r') as fp:
        config_content = fp.readlines()

        _size = tuple([int(i) for i in config_content[0].strip().split()])
        _shape = tuple([int(i) for i in config_content[1].strip().split()])
        _update_interval = tuple(int(i) for i in config_content[2].strip())
        _stock_codes = tuple(i.strip() for i in config_content[3:])

        if len(_size) != 2:
            raise ValueError(
                'Size of window got ' + str(_size) + ', expect two numbers like 1024 768'
            )
        if len(_shape) != 2:
            raise ValueError(
                'Shape of chart got ' + str(_shape) + ', expect two numbers like 4 4'
            )
        if _update_interval[0] < 0:
            raise ValueError(
                'Update interval got' + str(_update_interval) + ', expect a positive integer like 5'
            )
        if len(_stock_codes) != _shape[0] * _shape[1]:
            raise ValueError(
                'Number of stocks got ' + str(len(_stock_codes)) + ', expect ' + str(_shape[0] * _shape[1])
            )

    return _size, _shape, _update_interval, _stock_codes


def _setup_window():
    _window = tk.Tk()

    _window.geometry('x'.join([str(i) for i in size]))
    _window.resizable(False, False)
    # _window.wm_state('iconic')

    return _window


def _get_stock_image(stock_code):
    url = 'https://image.sinajs.cn/newchart/min/n/' + stock_code + '.gif'

    headers = {
        'authority': 'image.sinajs.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    proxies = {
        'http': None,
        'https': None
    }

    r = requests.get(url, headers=headers, proxies=proxies)
    image_bytes = io.BytesIO(r.content)
    img = Image.open(image_bytes)

    return img


def _update():
    global canvas, window

    if canvas is None:
        canvas = tk.Canvas(window, width=size[0], height=size[1])
        canvas.pack()

    window.image_ = []

    images = [_get_stock_image(stock_code).resize((size[0] // shape[0], size[1] // shape[1]), Image.ANTIALIAS) for
              stock_code in stock_codes]
    tk_images = [ImageTk.PhotoImage(image=image) for image in images]

    for i, image in enumerate(tk_images):
        window.image_.append(image)  # Avoid garbage collection
        row, col = i // shape[0], i % shape[0]

        canvas.create_image((row * size[0] // shape[0], col * size[1] // shape[1]), image=image, anchor='nw')

    window.title('Stock (data source: sina).' + ' Updated at ' + str(time.asctime()))

    window.after(1000 * update_interval[0], _update)


def main():
    _update()
    window.bind('<Escape>', lambda x: window.iconify())
    window.mainloop()


# Make configures as global variables
config = _read_config()
size, shape, update_interval, stock_codes = config
window = _setup_window()
canvas = None

if __name__ == '__main__':
    main()
