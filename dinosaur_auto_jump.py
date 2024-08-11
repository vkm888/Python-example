# auto jump Dinosaur T-Rex
# Використання бібліотеки pyautogui для натискання клавіш та pillow для обробки зображень
# '`' для start/finish чітера
# tkinter для відображення "пітонівського зору" м окреме вікно виводить що саме потрапило у вказані координати перед натисканням пробілу
# webbrowser для відкриття сторінки     https://dinorunner.com

import keyboard
import pyautogui
from PIL import ImageGrab, ImageOps, ImageTk
import tkinter as tk
import time
import numpy as np
# import winsound
import webbrowser

# start/finish при натисканні " ` "
work = False
def change():
    global work
    work = not work
keyboard.add_hotkey('`', change)

# Координати ділянки екрану
box = (733, 383, 800, 420)

# Створити головне вікно Tkinter
root = tk.Tk()
root.title("Скріншот області екрану")

# Встановити розташування вікна (наприклад, 300x200 розмір і розташування вікна на 100 пікселів зліва і 100 пікселів зверху)
root.geometry("300x200+1100+800")

# Створити віджет Label для відображення значення
color_label = tk.Label(root, text="Сумарне значення кольору: ")
color_label.pack()

# Створити віджет Label для відображення зображення
image_label = tk.Label(root)
image_label.pack()

# Функція для оновлення скріншоту і відображення значення
def update_screenshot():
    screenshot = ImageGrab.grab(box)
    gray_image = ImageOps.grayscale(screenshot)
    a = np.array(gray_image.getcolors())

    # Оновити текст у Label для значення кольору
    color_sum = a.sum()
    color_label.config(text=f"Сумарне значення кольору: {color_sum}")

    # Оновити зображення у Label для відображення скріншоту
    tk_image = ImageTk.PhotoImage(screenshot)
    image_label.config(image=tk_image)
    image_label.image = tk_image  # Зберегти посилання на зображення

    root.update_idletasks()
    root.update()

# Функція "Натискання пробілу"
def press_space():
    print("Перешкода виявлена! Натискання пробілу.")
    pyautogui.keyDown('space')
    time.sleep(0.05)
    pyautogui.keyUp('space')
    # winsound.Beep(1000, 100)  # Звуковий сигнал (1000 Гц, 100 мс)

# до кінця не реалізовано щоб T-Rex пригинав голову коли зверху летить птах, на зараз це більше заважа вчасно підстрибувати
# def press_down():
    # pyautogui.keyDown('down')
    # time.sleep(0.05)
    # pyautogui.keyUp('down')

# Функція виявлення перешкод через зміну значень пікселів
def detect_obstacle():
    # Координати прямокутника, де ми шукаємо перешкоди
    # box = (733, 383, 800, 420)
    image = ImageGrab.grab(box)
    gray_image = ImageOps.grayscale(image)
    a = np.array(gray_image.getcolors())

    # Логування значення сумарного колірного значення
    print("Сумарне значення кольору: ", a.sum())

    # Якщо перешкода наближається, значення пікселів змінюється
    if a.sum() > 2721:
        return True
    return False

# Відкриття нової вкладки в браузері з вказаним сайтом
webbrowser.open_new_tab("https://dinorunner.com")

# Затримка для переходу до гри
# time.sleep(2)

while True:
    if work:
        if detect_obstacle():
            update_screenshot()
            press_space()
        # else:
        #     press_down()