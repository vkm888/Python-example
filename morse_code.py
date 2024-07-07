import winsound
from pynput import keyboard
import tkinter as tk

# Таблиця азбуки Морзе
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'
}

# Перевірка на англійську розкладку
def is_english_char(char):
    return char.isalpha() and char.upper() in MORSE_CODE_DICT

# Функція відтворення коду Морзе
def play_morse_code(code, speed, dot_freq, dash_freq):
    dot_duration = int(100 * speed)
    dash_duration = int(300 * speed)
    for symbol in code:
        if symbol == '.':
            winsound.Beep(dot_freq, dot_duration)
        elif symbol == '-':
            winsound.Beep(dash_freq, dash_duration)
        winsound.Beep(dot_freq, dot_duration // 2)  # Затримка між символами

# Обробка натискання клавіші в режимі окремих клавіш
def on_press_key_mode(key):
    try:
        char = key.char.upper()
        if is_english_char(char):
            code = MORSE_CODE_DICT[char]
            key_label.config(text=f"Натиснута клавіша: {char}")
            morse_label.config(text=f"Код Морзе: {code}")
            play_morse_code(code, speed_scale.get(), dot_freq_scale.get(), dash_freq_scale.get())
    except AttributeError:
        pass  # Ігноруємо спеціальні клавіші

# Обробка натискання клавіші в режимі речень
def on_press_sentence_mode(key):
    global sentence
    try:
        char = key.char.upper()
        if is_english_char(char):
            sentence += char
            key_label.config(text=f"Натиснуті клавіші: {sentence}")
    except AttributeError:
        if key == keyboard.Key.enter:
            process_sentence()

# Обробка речення
def process_sentence():
    global sentence
    morse_sentence = ' '.join(MORSE_CODE_DICT[char] for char in sentence)
    morse_label.config(text=f"Код Морзе: {morse_sentence}")
    play_morse_code(morse_sentence, speed_scale.get(), dot_freq_scale.get(), dash_freq_scale.get())
    sentence = ''

# Перемикання режиму
def switch_mode():
    global mode, listener
    if mode == 'key':
        mode = 'sentence'
        switch_button.config(text="Режим: Речення")
    else:
        mode = 'key'
        switch_button.config(text="Режим: Клавіша")
    listener.stop()
    listener = keyboard.Listener(on_press=on_press_sentence_mode if mode == 'sentence' else on_press_key_mode)
    listener.start()

# Головна функція
def main():
    global root, key_label, morse_label, speed_scale, dot_freq_scale, dash_freq_scale, switch_button, mode, sentence, listener

    mode = 'key'
    sentence = ''

    # Налаштування вікна
    root = tk.Tk()
    root.title("Морзе Клавіатура")

    key_label = tk.Label(root, text="Натисніть клавішу", font=("Helvetica", 24))
    key_label.pack(pady=20)

    morse_label = tk.Label(root, text="Код Морзе: ", font=("Helvetica", 24))
    morse_label.pack(pady=20)

    speed_label = tk.Label(root, text="Швидкість відтворення:", font=("Helvetica", 14))
    speed_label.pack(pady=5)

    speed_scale = tk.Scale(root, from_=0.1, to=3.0, orient="horizontal", resolution=0.1)
    speed_scale.set(1.8)
    speed_scale.pack(pady=10)

    dot_freq_label = tk.Label(root, text="Частота крапки (Hz):", font=("Helvetica", 14))
    dot_freq_label.pack(pady=5)

    dot_freq_scale = tk.Scale(root, from_=100, to=2000, orient="horizontal", resolution=50)
    dot_freq_scale.set(2000)
    dot_freq_scale.pack(pady=10)

    dash_freq_label = tk.Label(root, text="Частота тире (Hz):", font=("Helvetica", 14))
    dash_freq_label.pack(pady=5)

    dash_freq_scale = tk.Scale(root, from_=100, to=2000, orient="horizontal", resolution=50)
    dash_freq_scale.set(750)
    dash_freq_scale.pack(pady=10)

    switch_button = tk.Button(root, text="Режим: Клавіша", command=switch_mode, font=("Helvetica", 14))
    switch_button.pack(pady=10)

    # Створюємо слухача клавіатури
    listener = keyboard.Listener(on_press=on_press_key_mode)
    listener.start()

    root.mainloop()

if __name__ == "__main__":
    main()
