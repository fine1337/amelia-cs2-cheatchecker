import tkinter as tk
from tkinter import simpledialog
import webbrowser
import os
import glob
import string
import threading
from datetime import datetime
from tkinter import ttk
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import os
import ctypes
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import tkinter as tk
from tkinter import simpledialog
import webbrowser
import os
import glob
import string
import threading
from datetime import datetime
from tkinter import ttk
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import ctypes

# Создаем основное окно
root = tk.Tk()
root.title("Amelia.SU - Проверка на читы")
root.geometry("800x600")
root.configure(bg="#111215")

# Создаем боковую панель
side_panel = tk.Frame(root, bg="#111215", width=200)
side_panel.pack(side="left", fill="y")

# Создаем основную область контента
content_area = tk.Frame(root, bg="#111215")
content_area.pack(side="right", expand=True, fill="both")

# Создаем метку состояния (по умолчанию пустую)
status_label = tk.Label(content_area, text="", font=("Arial", 12, "bold"), bg="#111215", fg="white")
status_label.pack(pady=10)

# Функция для открытия URL в браузере
def open_link(url):
    webbrowser.open_new(url)

# Функция для отображения информации
def show_info():
    for widget in content_area.winfo_children():
        widget.destroy()
    
    header = tk.Label(content_area, text="Информация", font=("Arial", 16, "bold"), bg="#111215", fg="white")
    header.pack(fill="x")

    info_text = (
        "Creator of project - fine1337\n"
        "Version - V1.0\n"
        "Hash - $dnq8391@\n"
        "Subjection - culturing\n"
        "Все апдейты будут выходить в телеграмм канале - https://t.me/amelia_project"
    )

    info_label = tk.Label(content_area, text=info_text, font=("Arial", 12, "bold"), bg="#111215", fg="white", justify="left")
    info_label.pack(pady=20, padx=20, anchor="w")

# Функция для отображения программ
def show_programs():
    for widget in content_area.winfo_children():
        widget.destroy()
    
    header = tk.Label(content_area, text="Программы", font=("Arial", 16, "bold"), bg="#111215", fg="white")
    header.pack(fill="x")

    programs = [
        ("ExecutedProgramsList", "Сбор информации об исполняемых программах ПК.", "https://www.nirsoft.net/utils/executed_programs_list.html"),
        ("Everything", "Индексация всех файлов и поиск по их именам.", "https://www.voidtools.com/"),
        ("USBDeview", "Вывод списка всех USB-устройств, когда-либо подключенных к ПК.", "https://www.nirsoft.net/utils/usb_devices_view.html"),
        ("ShellBag Analyzer", "Анализ ShellBag для управления следами использования системы.", "https://www.sans.org/tools/shellbag-analyzer/"),
        ("UserAssistView", "Извлечение и отображение записей UserAssist.", "https://www.nirsoft.net/utils/userassist_view.html"),
        ("AnyDesk", "Простая программа для удаленного управления ПК.", "https://anydesk.com/"),
        ("JumpListsView", "Показ всех Jump Lists на ПК.", "https://www.nirsoft.net/utils/jump_lists_view.html"),
        ("LastActivityView", "Отображение последних действий пользователя.", "https://www.nirsoft.net/utils/computer_activity_view.html"),
        ("USBDriveLog", "Список всех USB-устройств, подключенных к ПК.", "https://www.nirsoft.net/utils/usb_drive_log.html"),
        ("SystemInformer", "Получение системной информации о ПК.", "https://systeminformer.sourceforge.io/"),
        ("Process Hacker", "Мощный менеджер процессов для Windows.", "https://processhacker.sourceforge.io/")
    ]

    for program_name, program_description, program_url in programs:
        program_frame = tk.Frame(content_area, bg="#131417", padx=10, pady=10)
        program_frame.pack(fill="x", pady=5)
        
        link_label = tk.Label(program_frame, text=program_name, font=("Arial", 12, "bold"), bg="#131417", fg="#a9afb6", cursor="hand2")
        link_label.pack(anchor="w")
        link_label.bind("<Button-1>", lambda e, url=program_url: open_link(url))
        
        tk.Label(program_frame, text=program_description, bg="#131417", fg="#ffffff").pack(anchor="w")

# Функция для получения всех доступных дисков
def get_all_drives():
    # Получение списка всех доступных дисков
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in range(26):
        if bitmask & (1 << letter):
            drives.append(f"{chr(65 + letter)}:\\")
    return drives

# Функция для получения информации о файле
def get_file_info(file_path):
    try:
        stats = os.stat(file_path)
        creation_time = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        last_access_time = datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
        return file_path, creation_time, last_access_time
    except Exception as e:
        return file_path, "Неизвестно", "Неизвестно"

# Функция для выполнения поиска в фоновом потоке
def search_files(keywords, callback):
    search_results = []
    drives = get_all_drives()
    
    for drive in drives:
        # Исключаем системные каталоги из поиска
        if drive in ["C:\\Windows\\"]:
            continue
        
        for keyword in keywords:
            try:
                files = glob.glob(f"{drive}**/*{keyword}*", recursive=True)
                if files:
                    for file in files:
                        file_info = get_file_info(file)
                        search_results.append(file_info)
            except Exception as e:
                print(f"Ошибка при поиске в {drive}: {e}")
    
    # Обновляем результаты поиска в основном потоке
    root.after(0, callback, search_results)

# Функция для обновления UI с результатами поиска
def update_search_results(search_results, title):
    # Очистка области контента перед отображением результатов
    for widget in content_area.winfo_children():
        widget.destroy()

    # Заголовок результатов поиска
    header = tk.Label(content_area, text=title, font=("Arial", 16, "bold"), bg="#111215", fg="white")
    header.pack(fill="x")
    
    if search_results:
        # Отображение каждого результата в отдельной метке
        for file_path, creation_time, last_access_time in search_results:
            file_info = f"Файл: {file_path}\nДата создания: {creation_time}\nПоследний запуск: {last_access_time}"
            file_label = tk.Label(content_area, text=file_info, font=("Arial", 12, "bold"), bg="#111215", fg="white", wraplength=700, justify="left")
            file_label.pack(anchor="w", pady=5, padx=20)
    else:
        tk.Label(content_area, text="Файлы не найдены.", font=("Arial", 12, "bold"), bg="#111215", fg="white").pack(pady=20)

    # Обновляем текст метки состояния
    status_label.config(text="Поиск завершен.")

# Функция для автоматического поиска
def automatic_search():
    keywords = [
        "ESP", "Midnight Yeahnot", "VRedux", "Avira Neverlose", "ESPdX", "Legend",
        "EGHack", "nixware.cc", "RAGER", ".ahk", "PhoenixHack OmniAim", "OBR", "OneByteRadar",
        "NAIM EZinjector", "Reborn", "OneByteWall", "Hack", "Multihacklanyx.gg", "Ext. ExtrimHack",
        "EZfrags", "Nitamal", "FREEQN", "Aquila", "FRUX", "hack", "cheat", "чит", "Aimware",
        "Skeet", "gamesense", "Aurora", "SpirtHack", "Fatality", "OneTap", "Eternity", "Sockrpg",
        "Demonside.us", "Bhop", "BunnyHop", "AviraSAMOWARE", "ExLoader.amc", "freeqnlimgui.ini",
        "hacklethereal", "satano", "vredux", "nAimmy", "obrlekknod", "xone", "NAIM", "reborn",
        "AutoHotKey", "lvictorial", "ragerlespdx", "winnerfreelezcheats", "lexternallampetamin",
        "lketer", "vredux", "onemacro", "fecurity", "hellhit", "hellhack", "VTA", "VACnet",
        "Iniurialinterium", "Injector", "Osiris", "HackShield", "limguil", "Aimware", "fOrgOtten",
        "Infinity", "Vengeance", "Furiousleghack", "IEZfrags", "RHcheats", "Xenon", "Vivi", "HellHacks",
        "Synetix", "Ghosting", "Feliz", "Noobware", "Virtua", "ETernal", "Fallen", "LegitGuard", "Siphon",
        "Calypso", "OverClock", "Abyss", "NetHack", "HellHack", "XenoTech", "Snipe", "UltraKiller",
        "Nexware", "AdvancedKiller", "TrueHacks", "Radiance", "Phantom", "Hacker'sLab", "Astro", "Luminix",
        "CyberElite", "Shadow", "Nimble", "Paradise", "Nebula", "Quantum", "Vortex", "GenEx", "Phoenix",
        "Specter", "Eclipse", "Aether", "Helix", "Tranquil", "Legion", "Xero", "Vortex", "Ethereal",
        "Eternity", "HackXtreme", "EZC", "Alphahacks", "Nimbel", "VirusKiller",
        "OverKill", "InfiniteCheats", "Xtrm", "Apelion", "Ligma", "Jensware", "Vikavich", "Panzer" "en1gma-tech"
    ]
    
    
    # Обновляем текст метки состояния
    status_label.config(text="Поиск запущен...")
    
    def search_complete(results):
        update_search_results(results, "Результаты автоматического поиска")
    
    # Запуск поиска в фоновом потоке
    search_thread = threading.Thread(target=search_files, args=(keywords, search_complete))
    search_thread.start()

def manual_search():
    file_name = simpledialog.askstring("Ручной поиск", "Введите имя файла для поиска:")
    
    if file_name:
        status_label.config(text="Поиск запущен...")
        
        def search_complete(results):
            update_search_results(results, "Результаты ручного поиска")
        
        search_thread = threading.Thread(target=search_files, args=([file_name], search_complete))
        search_thread.start()

def read_vdf_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return content

def parse_vdf_content(content):
    accounts = []
    lines = content.splitlines()
    
    current_entry = {}
    entry_started = False

    for line in lines:
        line = line.strip()
        
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith('//'):
            continue
        
        if line.startswith('"765'):
            if entry_started and current_entry:
                accounts.append(current_entry)
                current_entry = {}
            entry_started = True
            current_entry['id'] = line.strip('"')
        elif entry_started:
            if '"' in line:
                parts = line.split('"', 2)
                if len(parts) >= 3:
                    key = parts[1].strip()
                    value = parts[2].strip()
                    current_entry[key] = value
    
    if entry_started and current_entry:
        accounts.append(current_entry)
    
    return accounts

def show_steam_accounts():
    for widget in content_area.winfo_children():
        widget.destroy()

    header = tk.Label(content_area, text="Steam Аккаунты", font=("Arial", 16, "bold"), bg="#111215", fg="white")
    header.pack(fill="x")

    account_frame = tk.Frame(content_area, bg="#131417", padx=10, pady=10)
    account_frame.pack(fill="x", pady=5)

    file_path = r'C:\Program Files (x86)\Steam\config\loginusers.vdf'
    try:
        content = read_vdf_file(file_path)
        accounts = parse_vdf_content(content)

        tree = ttk.Treeview(content_area, columns=("ID", "Account Name", "Persona Name", "Allow Auto Login"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Account Name", text="Account Name")
        tree.heading("Persona Name", text="Persona Name")
        tree.heading("Allow Auto Login", text="Allow Auto Login")

        tree.pack(fill="both", expand=True)

        for account in accounts:
            tree.insert("", "end", values=(
                account.get('id', 'Unknown'),
                account.get('AccountName', 'Unknown'),
                account.get('PersonaName', 'Unknown'),
                account.get('AllowAutoLogin', 'Unknown')
            ))

    except Exception as e:
        error_label = tk.Label(content_area, text=f"Ошибка при парсинге файла: {e}", font=("Arial", 12, "bold"), bg="#111215", fg="red")
        error_label.pack()




# Функция для отображения поиска
def show_search():
    for widget in content_area.winfo_children():
        widget.destroy()
    
    header = tk.Label(content_area, text="Поиск", font=("Arial", 16, "bold"), bg="#111215", fg="white")
    header.pack(fill="x")

    button_frame = tk.Frame(content_area, bg="#111215")
    button_frame.pack(pady=20)

    auto_button = tk.Button(button_frame, text="Автоматический поиск", font=("Arial", 12, "bold"), bg="#131417", fg="white", command=automatic_search)
    auto_button.pack(side="left", padx=10)

    manual_button = tk.Button(button_frame, text="Ручной поиск", font=("Arial", 12, "bold"), bg="#131417", fg="white", command=manual_search)
    manual_button.pack(side="left", padx=10)

    # Пересоздаем метку состояния в функции show_search
    global status_label
    status_label = tk.Label(content_area, text="", font=("Arial", 12, "bold"), bg="#111215", fg="white")
    status_label.pack(pady=10)

def show_additional():
    for widget in content_area.winfo_children():
        widget.destroy()

    header = tk.Label(content_area, text="Дополнительно", font=("Arial", 16, "bold"), bg="#111215", fg="white")
    header.pack(fill="x")
    
    resources = [
        ("Поддержка Проекта", "https://t.me/ragotn"),
        ("Программа Написана на", "https://www.python.org/"),
        ("Скачать Чекер", "https://t.me/+PZgIJ5nVjrs2OTE0")
    ]
    
    for resource_name, resource_url in resources:
        resource_frame = tk.Frame(content_area, bg="#131417", padx=10, pady=10)
        resource_frame.pack(fill="x", pady=5)
        
        link_label = tk.Label(resource_frame, text=resource_name, font=("Arial", 12, "bold"), bg="#131417", fg="#a9afb6", cursor="hand2")
        link_label.pack(anchor="w")
        link_label.bind("<Button-1>", lambda e, url=resource_url: open_link(url))

def get_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in range(26):
        if bitmask & (1 << letter):
            drives.append(f"{chr(65 + letter)}:\\")
    return drives

def find_process_hacker():
    drives = get_drives()
    for drive in drives:
        print(f"Checking {drive}...")  # Отладочная информация
        for root, dirs, files in os.walk(drive):
            if 'ProcessHacker.exe' in files:
                print(f"Found at {os.path.join(root, 'ProcessHacker.exe')}")  # Отладочная информация
                return os.path.join(root, 'ProcessHacker.exe')
    return None

def open_process_hacker():
    path = find_process_hacker()
    if path:
        try:
            subprocess.Popen(path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть Process Hacker: {e}")
    else:
        messagebox.showinfo("Информация", "Process Hacker не найден на вашем компьютере.")

def threaded_open_process_hacker():
    threading.Thread(target=open_process_hacker).start()

def show_logs():
    for widget in content_area.winfo_children():
        widget.destroy()

    header = tk.Label(content_area, text="Логи", font=("Arial", 16, "bold"), bg="#111215", fg="white")
    header.pack(fill="x")

    log_frame = tk.Frame(content_area, bg="#131417", padx=10, pady=10)
    log_frame.pack(fill="both", expand=True, pady=20, padx=20)

    try:
        logo_img = tk.PhotoImage(file="icons/hacker.png")
        logo_label = tk.Label(log_frame, image=logo_img, bg="#131417")
        logo_label.image = logo_img
        logo_label.pack()
    except tk.TclError:
        error_label = tk.Label(log_frame, text="Ошибка при загрузке логотипа.", font=("Arial", 12), bg="#131417", fg="red")
        error_label.pack()

    instruction_text = tk.Label(log_frame, text="Для дальнейших действий откройте Process Hacker.", font=("Arial", 12), bg="#131417", fg="white")
    instruction_text.pack(pady=10)

    open_button = tk.Button(log_frame, text="Открыть программу", font=("Arial", 12), bg="#131417", fg="white", command=threaded_open_process_hacker)
    open_button.pack(pady=10)


# Добавляем кнопки навигации на боковую панель
buttons = [
    ("Информация", show_info),
    ("Программы", show_programs),
    ("Поиск", show_search),
    ("Дополнительно", show_additional),
    ("Аккаунты", show_steam_accounts),
    ("Логи", show_logs)
]

for button in side_panel.winfo_children():
    button.pack_configure(pady=20)

for text, command in buttons:
    btn = tk.Button(side_panel, text=text, font=("Arial", 12, "bold"), bg="#131417", fg="white", activebackground="#858de4", activeforeground="white", bd=0, command=command)
    btn.pack(fill="x", padx=10, pady=10)

# Изначально показываем раздел "Программы"
show_programs()

# Запускаем основной цикл
root.mainloop()