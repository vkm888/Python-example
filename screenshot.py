from PIL import ImageGrab
import time

time.sleep(5)

# Координати ділянки екрану
# box = (720, 370, 800, 420)  # Координати прямокутника, де (left, top, right, bottom) визначають область екрану.
box = (733, 383, 800, 420)

# Зробити скріншот цієї області
screenshot = ImageGrab.grab(box)

# Зберегти скріншот як зображення у файл screen_area.png у поточній директорії.
screenshot.save("screen_area.png")

# Відкрити зображення, щоб побачити область
screenshot.show()
