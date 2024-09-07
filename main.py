import keyboard
import pyperclip
import time
import os
import sys
from loguru import logger

logger.remove()

def custom_log_format(record):
    message = record["message"]
    if "Скрипт запущен" in message or "Нажмите Alt+9 для включения/выключения." in message:
        return f"<yellow>{record['time']:YYYY-MM-DD HH:mm:ss} {message}</yellow>\n"
    elif "Скрипт выключен" in message:
        return f"<red>{record['time']:YYYY-MM-DD HH:mm:ss} {message}</red>\n"
    elif "Скрипт включен" in message:
        return f"<blue>{record['time']:YYYY-MM-DD HH:mm:ss} {message}</blue>\n"
    elif "Такого значения нету в списке замен" in message:
        return f"<white>{record['time']:YYYY-MM-DD HH:mm:ss} {message}</white>\n"
    elif "Активация замены текста" in message:
        return f"<green>{record['time']:YYYY-MM-DD HH:mm:ss} {message}</green>\n"
    elif "Считано из буфера" in message:
        return f"<cyan>{record['time']:YYYY-MM-DD HH:mm:ss} {message}</cyan>\n"
    else:
        return f"<white>{record['time']:YYYY-MM-DD HH:mm:ss} {message}</white>\n"

#Цветное отображение. False на True измени
logger.add(sys.stderr, colorize=True, format=custom_log_format)

enabled = True

def load_replacements():
    replacements = {}
    if os.path.exists("list.txt"):
        with open("list.txt", "r", encoding="utf-8") as file:
            for line in file:
                if "=" in line:
                    key, value = map(str.strip, line.split("="))
                    replacements[key] = value
    return replacements

def replace_selected_text():
    keyboard.send("ctrl+c")
    time.sleep(0.05)
    selected_text = pyperclip.paste().strip()
    logger.info(f"Считано из буфера: '{selected_text}'")
    replacements = load_replacements()
    replaced = False

    for key, value in replacements.items():
        if selected_text == key:
            pyperclip.copy(value)
            keyboard.send("ctrl+v")
            logger.info(f"Успешная замена значения '{key}' на '{value}'")
            replaced = True
            break
    
    if not replaced:
        logger.warning("Такого значения нету в списке замен")

def toggle_script():
    global enabled
    enabled = not enabled
    status = "включен" if enabled else "выключен"
    logger.info(f"Скрипт {status}")

def check_and_replace():
    if enabled and keyboard.is_pressed('win+alt'):
        logger.info("Активация замены текста")
        replace_selected_text()
    else:
        logger.info("Замена текста не активирована")

keyboard.add_hotkey("alt+9", toggle_script, suppress=True)
keyboard.add_hotkey("win+alt", check_and_replace)

try:
    logger.info("Скрипт запущен. Нажмите Alt+9 для включения/выключения.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Скрипт остановлен.")