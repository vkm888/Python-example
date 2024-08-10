# код виконує авто клік мишки
# '`' для start/finish
# для перевірки відкривається наступний сайт  https://clickspeedtest.com/10-seconds.html

import keyboard
import mouse
import time
import webbrowser

# Відкрити нову вкладку в браузері з вказаним сайтом
webbrowser.open_new_tab("https://clickspeedtest.com/10-seconds.html")

def change():
    global work
    work = not work

work = False
keyboard.add_hotkey('`', change)

while True:
    if work:
        mouse.click(button='left')
        time.sleep(0.05)