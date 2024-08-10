# auto jump Dinosaur T-Rex
# Використання бібліотеки pyautogui для натискання клавіш та pillow для обробки зображень
# '`' для start/finish чітера
# tkinter для відображення "пітонівського зору" м окреме вікно виводить що саме потрапило у вказані координати перед натисканням пробілу
# webbrowser для відкриття сторінки https://dinorunner.com

import keyboard
import pyautogui
from PIL import ImageGrab, ImageOps, ImageTk
import tkinter as tk
import time
import numpy as np
import winsound
import webbrowser


# Координати ділянки екрану
box = (733, 383, 800, 420)

# Створити головне вікно Tkinter
root = tk.Tk()
root.title("Скріншот області екрану")

# Встановити розташування вікна (наприклад, 300x200 розмір і розташування вікна на 100 пікселів зліва і 100 пікселів зверху)
root.geometry("300x200+1100+800")

# Створити віджет Label
label = tk.Label(root)
label.pack()

# Функція оновлення зображення для вікна tkinter
def update_screenshot():
    screenshot = ImageGrab.grab(box)
    tk_image = ImageTk.PhotoImage(screenshot)
    label.config(image=tk_image)
    label.image = tk_image  # Зберегти посилання на зображення, щоб воно не видалилось збирачем сміття
    root.update_idletasks()
    root.update()

def change():
    global work
    work = not work

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

def detect_obstacle():
    # Координати прямокутника, де ми шукаємо перешкоди
    box = (733, 383, 800, 420) #(280, 400, 400, 450)
    image = ImageGrab.grab(box)
    gray_image = ImageOps.grayscale(image)
    a = np.array(gray_image.getcolors())

    # Логування значення сумарного колірного значення
    print("Сумарне значення кольору: ", a.sum())

    # Якщо перешкода наближається, значення пікселів змінюється
    if a.sum() > 2721: # 1447  3202
        return True
    return False

# start/finish при натисканні " ` "
work = False
keyboard.add_hotkey('`', change)

# Відкрити нову вкладку в браузері з вказаним сайтом
webbrowser.open_new_tab("https://dinorunner.com")

time.sleep(2)  # Затримка для переходу до гри

while True:
    if work:
        if detect_obstacle():
            update_screenshot()
            press_space()
        # else:
        #     press_down()