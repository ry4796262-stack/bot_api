import os
import platform
import time
import telebot
import psutil
import pyautogui

TOKEN = ''
ID = 

bot = telebot.TeleBot(TOKEN)

def check_user(message):
    return message.chat.id == ID

def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    ram_used = memory.used / (1024 ** 3)
    ram_total = memory.total / (1024 ** 3)
    disk = psutil.disk_usage('/')
    
    net = psutil.net_io_counters()
    net_sent = net.bytes_sent / (1024 ** 2)
    net_recv = net.bytes_recv / (1024 ** 2)
    
    return (
        f"*Состояние ПК*\n\n"
        f"*CPU:* {cpu_usage}%\n"
        f"*RAM:* {ram_usage}% ({ram_used:.1f} GB / {ram_total:.1f} GB)\n"
        f"*Диск C:* {disk.percent}%\n"
        f"*Сеть (Отправлено / Получено):* {net_sent:.1f} MB / {net_recv:.1f} MB"
    )

def take_screenshot(filename='screenshot.png'):
    pyautogui.screenshot(filename)
    return filename

def shutdown_system(delay=5):
    if platform.system() == 'Windows':
        os.system(f'shutdown /s /t {delay}')
    else:
        os.system('shutdown -h +0')


# --- Telegram-бот с защитой ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_user(message):
        bot.reply_to(message, "Пошел нахуй")
        return
        
    bot.reply_to(message, 
        "Бот для удаленного контроля пк.\n\n"
        "команды:\n"
        "/stats - данные системы\n"
        "/screenshot - скриншот\n"
        "/shutdown - выключить пк"
    )

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if not check_user(message):
        return
    stats_text = get_system_stats()
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

@bot.message_handler(commands=['screenshot'])
def send_screenshot(message):
    if not check_user(message):
        return
    bot.reply_to(message, "делаю скрин")
    screenshot_path = take_screenshot()
    
    with open(screenshot_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption =  'вот скриншот')
    
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)

@bot.message_handler(commands=['shutdown'])
def shutdown_pc(message):
    if not check_user(message):
        return
    bot.reply_to(message, "пк щас выключится")
    time.sleep(2)
    shutdown_system(delay=5)


if __name__ == '__main__':
    bot.infinity_polling()