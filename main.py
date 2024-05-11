import tkinter as tk
from tkinter import messagebox, filedialog


def do_nothing(*args):
    pass


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Text editor')
        self.root.geometry('600x800')

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
        self.root.bind('<Control-c>', do_nothing)
        self.root.bind('<Control-v>', do_nothing)
        self.root.bind('<Control-x>', do_nothing)

    def init_menu(self):
        main_menu = tk.Menu(self.root)

        file_menu = tk.Menu(main_menu, tearoff=0)
        file_menu.add_command(label='Открыть', command=self.open_file)
        file_menu.add_command(label='Сохранить', command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Закрыть', command=self.close_window)

        view_menu = tk.Menu(main_menu, tearoff=0)
        view_menu_sub = tk.Menu(view_menu, tearoff=0)
        font_menu_sub = tk.Menu(view_menu, tearoff=0)
        view_menu_sub.add_command(label='Тёмная', command=lambda: self.change_theme('dark'))
        view_menu_sub.add_command(label='Светлая', command=lambda: self.change_theme('light'))
        view_menu.add_cascade(label='Тема', menu=view_menu_sub)

        font_menu_sub.add_command(label='Arial', command=lambda: self.change_font('Arial'))
        font_menu_sub.add_command(label='Times New Roman', command=lambda: self.change_font('TNR'))
        view_menu.add_cascade(label='Шрифт', menu=font_menu_sub)

        main_menu.add_cascade(label='Файл', menu=file_menu)
        main_menu.add_cascade(label='Вид', menu=view_menu)
        self.root.config(menu=main_menu)

    def run(self):
        self.root.mainloop()

    def keypress(self, event):
        print(event.keycode)
        if event.keycode == 86:
            event.widget.event_generate('<<Paste>>')
        elif event.keycode == 67:
            event.widget.event_generate('<<Copy>>')
        elif event.keycode == 88:
            event.widget.event_generate('<<Cut>>')
        elif event.keycode == 65:
            event.widget.event_generate('<<SelectAll>>')
        elif event.keycode == 90:
            try:
                self.text_field.edit_undo()
            except tk.TclError:
                pass
        elif event.keycode == 89:
            try:
                self.text_field.edit_redo()
            except tk.TclError:
                pass

    def change_theme(self, theme: str) -> None:
        self.text_field['bg'] = view_colors[theme]['text_bg']
        self.text_field['fg'] = view_colors[theme]['text_fg']
        self.text_field['insertbackground'] = view_colors[theme]['cursor']
        self.text_field['selectbackground'] = view_colors[theme]['select_bg']

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
