from PIL import ImageGrab, ImageTk
import tkinter as tk

# Координати ділянки екрану
box = (340, 410, 450, 450)

# Створити головне вікно Tkinter
root = tk.Tk()
root.title("Скріншот області екрану")

# Встановити розташування вікна (наприклад, 300x200 розмір і розташування вікна на 100 пікселів зліва і 100 пікселів зверху)
root.geometry("300x200+1100+800")

# Створити віджет Label
label = tk.Label(root)
label.pack()

# Функція оновлення зображення
def update_screenshot():
    screenshot = ImageGrab.grab(box)
    tk_image = ImageTk.PhotoImage(screenshot)
    label.config(image=tk_image)
    label.image = tk_image  # Зберегти посилання на зображення, щоб воно не видалилось збирачем сміття
    root.update_idletasks()
    root.update()

while True:
    update_screenshot()
