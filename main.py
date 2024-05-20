import tkinter as tk
from tkinter import messagebox, filedialog
from re import finditer

import pygments.lexers
from chlorophyll import CodeView


def do_nothing(*args):
    pass


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Блокнот')
        self.root.geometry('600x800')
        self.cur_lexer = None

        self.init_menu()

        self.frame_text = tk.Frame(self.root)
        self.frame_text.pack(fill=tk.BOTH, expand=1)
        self.text_field = tk.Text(self.frame_text,
                                  bg='white', fg='black',
                                  padx=10, pady=10, wrap=tk.WORD,
                                  insertbackground='#a5a5a5',
                                  selectbackground='#3b51bf', spacing3=7,
                                  width=20,
                                  font='Arial 14',
                                  undo=True)
        self.text_field.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

        scroll = tk.Scrollbar(self.frame_text, command=self.text_field.yview, orient=tk.VERTICAL)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.text_field.config(yscrollcommand=scroll.set)

        self.root.bind('<Control-KeyPress>', self.keypress)
        self.root.bind('<Control-z>', do_nothing)
        self.root.bind('<Control-x>', do_nothing)
        self.root.bind('<Control-c>', do_nothing)
        self.root.bind('<Control-v>', do_nothing)

    def init_menu(self):
        main_menu = tk.Menu(self.root)

        file_menu = tk.Menu(main_menu, tearoff=0)
        file_menu.add_command(label='Открыть', command=self.open_file)
        file_menu.add_command(label='Сохранить', command=self.save_file)
        file_menu.add_command(label='Новое окно', command=self.new_window)
        file_menu.add_separator()
        file_menu.add_command(label='Закрыть', command=self.close_window)

        edit_menu = tk.Menu(main_menu, tearoff=0)
        edit_menu.add_command(label='Отменить', command=self.undo)
        edit_menu.add_separator()
        edit_menu.add_command(label='Вырезать', command=lambda: self.text_field.event_generate('<<Cut>>'))
        edit_menu.add_command(label='Копировать', command=lambda: self.text_field.event_generate('<<Copy>>'))
        edit_menu.add_command(label='Вставить', command=lambda: self.text_field.event_generate('<<Paste>>'))
        edit_menu.add_separator()
        edit_menu.add_command(label='Найти...', command=self.find_text)
        edit_menu.add_command(label='Заменить...', command=self.replace_text)

        view_menu = tk.Menu(main_menu, tearoff=0)
        view_menu_sub = tk.Menu(view_menu, tearoff=0)
        font_menu_sub = tk.Menu(view_menu, tearoff=0)
        view_menu_sub.add_command(label='Тёмная', command=lambda: self.change_theme('dark'))
        view_menu_sub.add_command(label='Светлая', command=lambda: self.change_theme('light'))
        view_menu.add_cascade(label='Тема', menu=view_menu_sub)

        font_menu_sub.add_command(label='Arial', command=lambda: self.change_font('Arial'))
        font_menu_sub.add_command(label='Times New Roman', command=lambda: self.change_font('TNR'))
        view_menu.add_cascade(label='Шрифт', menu=font_menu_sub)

        develop_menu_sub = tk.Menu(view_menu, tearoff=0)
        develop_menu_sub.add_command(label='Python', command=lambda: self.development(pygments.lexers.PythonLexer))
        develop_menu_sub.add_command(label='C++', command=lambda: self.development(pygments.lexers.CppLexer))
        develop_menu_sub.add_command(label='Java', command=lambda: self.development(pygments.lexers.JavaLexer))
        view_menu.add_cascade(label='Разработка', menu=develop_menu_sub)

        main_menu.add_cascade(label='Файл', menu=file_menu)
        main_menu.add_cascade(label='Правка', menu=edit_menu)
        main_menu.add_cascade(label='Вид', menu=view_menu)
        self.root.config(menu=main_menu)

    def run(self):
        self.root.mainloop()

    def undo(self):
        try:
            self.text_field.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_field.edit_redo()
        except tk.TclError:
            pass

    def keypress(self, event):
        if event.keycode == 86:  # V
            event.widget.event_generate('<<Paste>>')
        elif event.keycode == 67:  # C
            event.widget.event_generate('<<Copy>>')
        elif event.keycode == 88:  # X
            event.widget.event_generate('<<Cut>>')
        elif event.keycode == 65:  # A
            event.widget.event_generate('<<SelectAll>>')
        elif event.keycode == 90:  # Z
            self.undo()
        elif event.keycode == 89:  # Y
            self.redo()
        elif event.keycode == 70:  # F
            self.find_text()

    def change_theme(self, theme: str) -> None:
        if not self.cur_lexer:
            self.text_field['bg'] = view_colors[theme]['text_bg']
            self.text_field['fg'] = view_colors[theme]['text_fg']
            self.text_field['insertbackground'] = view_colors[theme]['cursor']
            self.text_field['selectbackground'] = view_colors[theme]['select_bg']
        else:
            if theme == 'light':
                self.text_field.configure(color_scheme='ayu-light')
            else:
                self.text_field.configure(color_scheme='monokai')

    def change_font(self, font: str) -> None:
        self.text_field['font'] = fonts[font]['font']

    def close_window(self) -> None:
        answer = messagebox.askokcancel('Exit', 'Do you want to exit?')
        if answer:
            self.root.destroy()

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(title='Выбор файла',
                                               filetypes=(
                                                   ('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        if file_path:
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert('1.0', open(file_path, encoding='utf-8').read())

    def save_file(self) -> None:
        file_path = filedialog.asksaveasfilename(
            filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        file = open(file_path, 'w', encoding='utf-8')
        text = self.text_field.get('1.0', tk.END)
        file.write(text)
        file.close()

    def find_text(self):

        find_window = tk.Toplevel(self.root)
        find_window.geometry('300x88')
        find_window.title('Найти')

        find_label = tk.Label(find_window, text='Найти вхождения в тексте:')
        find_label.pack()

        find_entry = tk.Entry(find_window)
        find_entry.pack()

        lettercase_use = tk.BooleanVar()
        find_button = tk.Button(find_window, text='Найти',
                                command=lambda: self.search_text(find_entry.get(), lettercase_use))
        find_button.pack()

        lettercase_button = tk.Checkbutton(find_window, text='Не учитывать регистр', variable=lettercase_use)
        lettercase_button.pack()

        def close_window():
            self.text_field.tag_delete('selection')
            find_window.destroy()

        find_window.protocol('WM_DELETE_WINDOW', close_window)

    def search_text(self, text, lettercase_use):
        self.text_field.tag_delete('selection')
        data = self.text_field.get('1.0', tk.END)

        if lettercase_use.get():
            data = data.lower()
            text = text.lower()
        matches = finditer(text, data)
        for match in matches:
            self.text_field.tag_add("selection", f'1.0+{match.start()}c', f'1.0+{match.end()}c')
            self.text_field.tag_config("selection", background="#3295a8")

    def replace_text(self):

        replace_window = tk.Toplevel(self.root)
        replace_window.geometry('300x130')
        replace_window.title('Найти')

        find_label = tk.Label(replace_window, text='Заменить текст:', anchor='center')
        find_label.pack()

        tk.Label(replace_window, text='Что:').pack()
        find_entry = tk.Entry(replace_window)
        find_entry.pack()

        tk.Label(replace_window, text='Чем:').pack()
        replace_entry = tk.Entry(replace_window)
        replace_entry.pack()

        def edit_text():
            self.text_field.tag_delete('selection')
            new_text = self.text_field.get('1.0', tk.END).replace(find_entry.get(), replace_entry.get())
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert('1.0', new_text)
            self.search_text(replace_entry.get())

        replace_button = tk.Button(replace_window, text='Заменить', command=edit_text)
        replace_button.pack()

        def close_window():
            self.text_field.tag_delete('selection')
            replace_window.destroy()

        replace_window.protocol('WM_DELETE_WINDOW', close_window)

    def new_window(self):
        new_app = Application()
        new_app.run()

    def development(self, lexer):
        self.root.destroy()
        if self.cur_lexer != lexer:
            self.root = tk.Tk()
            self.root.title('Блокнот')
            self.root.geometry('600x800')
            self.cur_lexer = lexer

            self.init_menu()

            self.text_field = CodeView(self.root, lexer=lexer, color_scheme='monokai', undo=True)
            self.text_field.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

            self.root.bind('<Control-KeyPress>', self.keypress)
            self.root.bind('<Control-z>', do_nothing)
            self.root.bind('<Control-x>', do_nothing)
            self.root.bind('<Control-c>', do_nothing)
            self.root.bind('<Control-v>', do_nothing)
        else:
            self.__init__()


view_colors = {
    'dark': {
        'text_bg': 'black',
        'text_fg': '#bfbfbf',
        'cursor': '#ffffff',
        'select_bg': '#a0bddb'
    },
    'light': {
        'text_bg': 'white',
        'text_fg': 'black',
        'cursor': '#a5a5a5',
        'select_bg': '#3b51bf'
    }
}

fonts = {
    'Arial': {
        'font': ('Arial', '14')
    },
    'TNR': {
        'font': ('Times New Roman', '14')
    }
}

app = Application()
app.run()
