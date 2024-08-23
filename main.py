from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os

class Application():
    def __init__(self):
        self.root = Tk()
        self.root.title('zRAT')
        self.root.geometry('1200x720')
        self.root.resizable(width=False, height=False)

        # Определение пути к файлам
        if getattr(sys, 'frozen', False):
            # Если исполняемый файл запущен из PyInstaller
            bundle_dir = sys._MEIPASS
        else:
            # Если исполняемый файл запущен из исходного кода
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        # Иконка приложения
        self.icon_image = Image.open(os.path.join(bundle_dir, "icon.png"))  
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        self.root.iconphoto(False, self.icon_photo)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Стилизация вкладок
        self.style.configure("TNotebook", background="#2b2b2b")
        self.style.configure("TNotebook.Tab", background="#2b2b2b", foreground="#ffffff", padding=[10, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "#4CAF50")], foreground=[("selected", "#ffffff")])

        # Создание основного контейнера для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Создание первой вкладки
        self.main_frame = Frame(self.notebook, bg="#2b2b2b")
        self.notebook.add(self.main_frame, text='Главное')

        self.canvas = Canvas(self.main_frame, width=1200, height=675, bg='black')
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = Image.open(os.path.join(bundle_dir, "background.png"))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        font_header = ("Helvetica", 12, "bold")
        font_normal = ("Helvetica", 10)
        btn_color = "#4CAF50" 
        text_color = "#ffffff"
        bg_color = "#2b2b2b"

        # Изменяем стиль таблицы
        self.style.configure("Treeview", 
                             background=bg_color, 
                             foreground=text_color, 
                             fieldbackground=bg_color, 
                             rowheight=25)
        self.style.map("Treeview", background=[('selected', '#3e3e3e')])

        self.connection_list = ttk.Treeview(self.main_frame, columns=("IP", "OS", "Status"), show="headings", height=10)
        self.connection_list.heading("IP", text="IP")
        self.connection_list.heading("OS", text="OS")
        self.connection_list.heading("Status", text="Status")
        self.connection_list.column("IP", width=150)
        self.connection_list.column("OS", width=150)
        self.connection_list.column("Status", width=100)
        self.style.configure("Treeview.Heading", font=font_header, background=btn_color, foreground=text_color)

        self.connection_list.insert("", "end", values=("83.220.236.105", "Windows 10", "Connected"))
        self.connection_list.insert("", "end", values=("225.217.195.83", "Windows 10", "Idle"))

        self.canvas.create_window(50, 50, anchor="nw", window=self.connection_list)

        self.control_frame = Frame(self.main_frame, bg=bg_color)
        self.canvas.create_window(950, 25, anchor="nw", window=self.control_frame)

        self.button_style = {
            "font": font_normal, 
            "bg": btn_color,  
            "fg": text_color, 
            "bd": 0, 
            "highlightthickness": 0, 
            "width": 20, 
            "height": 2
        }

        self.command_button = Button(self.control_frame, text="Запустить команду", **self.button_style, command=self.run_command)
        self.command_button.pack(pady=5, padx=5)

        self.files_button = Button(self.control_frame, text="Просмотреть файлы", **self.button_style, command=self.view_files)
        self.files_button.pack(pady=5, padx=5)

        self.screen_button = Button(self.control_frame, text="Захват экрана", **self.button_style, command=self.capture_screen)
        self.screen_button.pack(pady=5, padx=5)

        self.network_button = Button(self.control_frame, text="Сетевые настройки", **self.button_style, command=self.network_settings)
        self.network_button.pack(pady=5, padx=5)

        self.update_button = Button(self.control_frame, text="Обновить статус", **self.button_style, command=self.update_status)
        self.update_button.pack(pady=5, padx=5)

        self.shutdown_button = Button(self.control_frame, text="Выключить", **self.button_style, command=self.shutdown_system)
        self.shutdown_button.pack(pady=5, padx=5)

        self.scrimers_button = Button(self.control_frame, text="Включить скримеры", **self.button_style, command=self.shutdown_system)
        self.scrimers_button.pack(pady=5, padx=5)

        self.openphoto_button = Button(self.control_frame, text="Открыть фото", **self.button_style, command=self.shutdown_system)
        self.openphoto_button.pack(pady=5, padx=5)

        # Поле ввода команды с фоном #2b2b2b
        self.command_entry = Entry(self.main_frame, width=50, font=font_normal, bd=2, relief="flat", bg=bg_color, fg=text_color)
        self.command_entry.place(x=50, y=350, height=30)

        self.send_command_button = Button(self.main_frame, text="Отправить команду", **self.button_style, command=self.send_command)
        self.send_command_button.place(x=400, y=350, height=30)

        self.connection_control_frame = Frame(self.main_frame, bg=bg_color)
        self.canvas.create_window(950, 475, anchor="nw", window=self.connection_control_frame)

        self.add_connection_button = Button(self.connection_control_frame, text="Добавить соединение", **self.button_style, command=self.add_connection)
        self.add_connection_button.pack(pady=5, padx=5)

        self.remove_connection_button = Button(self.connection_control_frame, text="Удалить соединение", **self.button_style, command=self.remove_connection)
        self.remove_connection_button.pack(pady=5, padx=5)

        self.update_connection_button = Button(self.connection_control_frame, text="Обновить соединение", **self.button_style, command=self.update_connection)
        self.update_connection_button.pack(pady=5, padx=5)

        self.status_label = Label(self.main_frame, text="Статус: Не выбрано", font=font_header, bg=bg_color, fg=text_color)
        self.canvas.create_window(50, 600, anchor="nw", window=self.status_label)

        self.log_text = Text(self.main_frame, height=10, width=80, font=font_normal, bg=bg_color, fg=text_color, bd=2, relief="flat")
        self.log_text.insert(END, "Лог консоли:\n")
        self.canvas.create_window(50, 400, anchor="nw", window=self.log_text)

        self.connection_list.bind('<<TreeviewSelect>>', self.on_select)

        # Создание второй вкладки
        self.builder_frame = Frame(self.notebook, bg="#2b2b2b")
        self.notebook.add(self.builder_frame, text='Билдер')

        # Пример содержимого второй вкладки
        self.builder_label = Label(self.builder_frame, text="Конструктор", font=font_header, bg=bg_color, fg=text_color)
        self.builder_label.pack(pady=20, padx=20)

        # Примерный билдер
        self.builder_options = Frame(self.builder_frame, bg=bg_color)
        self.builder_options.pack(pady=10, padx=20)

        self.option1_label = Label(self.builder_options, text="Опция 1:", font=font_normal, bg=bg_color, fg=text_color)
        self.option1_label.grid(row=0, column=0, padx=10, pady=5)

        self.option1_entry = Entry(self.builder_options, width=30, font=font_normal, bg="#3e3e3e", fg=text_color)
        self.option1_entry.grid(row=0, column=1, padx=10, pady=5)

        self.option2_label = Label(self.builder_options, text="Опция 2:", font=font_normal, bg=bg_color, fg=text_color)
        self.option2_label.grid(row=1, column=0, padx=10, pady=5)

        self.option2_entry = Entry(self.builder_options, width=30, font=font_normal, bg="#3e3e3e", fg=text_color)
        self.option2_entry.grid(row=1, column=1, padx=10, pady=5)

        self.builder_button = Button(self.builder_frame, text="Применить", font=font_normal)

    def apply_builder_settings(self):
        option1 = self.option1_entry.get()
        option2 = self.option2_entry.get()
        self.log_text.insert(END, f"Применены настройки: Опция 1 = {option1}")
        option2 = self.option2_entry.get()
        self.log_text.insert(END, f"Применены настройки: Опция 1 = {option1}, Опция 2 = {option2}\n")

    def run_command(self):
        self.log_text.insert(END, "Команда запущена на всех подключенных клиентах.\n")

    def view_files(self):
        self.log_text.insert(END, "Просмотр файлов запущен.\n")

    def capture_screen(self):
        self.log_text.insert(END, "Захват экрана выполнен.\n")

    def send_command(self):
        command = self.command_entry.get()
        if command:
            self.log_text.insert(END, f"Отправка команды: {command}\n")
            self.command_entry.delete(0, END)

    def network_settings(self):
        self.log_text.insert(END, "Сетевые настройки открыты.\n")

    def update_status(self):
        self.log_text.insert(END, "Статус обновлен.\n")

    def shutdown_system(self):
        self.log_text.insert(END, "Система будет выключена.\n")

    def add_connection(self):
        self.log_text.insert(END, "Добавлено новое соединение.\n")

    def remove_connection(self):
        selected_item = self.connection_list.selection()
        if selected_item:
            self.connection_list.delete(selected_item)
            self.log_text.insert(END, "Соединение удалено.\n")

    def update_connection(self):
        self.log_text.insert(END, "Соединение обновлено.\n")

    def on_select(self, event):
        selected_item = self.connection_list.selection()
        if selected_item:
            item = self.connection_list.item(selected_item)
            ip, os, status = item['values']
            self.status_label.config(text=f"Статус: IP={ip}, OS={os}, Status={status}")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.main()
