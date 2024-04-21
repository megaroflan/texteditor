import tkinter as tk
from tkinter import messagebox, filedialog


def change_theme(theme: str) -> None:
    text_field['bg'] = view_colors[theme]['text_bg']
    text_field['fg'] = view_colors[theme]['text_fg']
    text_field['insertbackground'] = view_colors[theme]['cursor']
    text_field['selectbackground'] = view_colors[theme]['select_bg']


def change_font(font: str) -> None:
    text_field['font'] = fonts[font]['font']


def close_window() -> None:
    answer = messagebox.askokcancel('Exit', 'Do you want to exit?')
    if answer:
        root.destroy()


def open_file() -> None:
    file_path = filedialog.askopenfilename(title='Выбор файла',
                                           filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
    if file_path:
        text_field.delete('1.0', tk.END)
        text_field.insert('1.0', open(file_path, encoding='utf-8').read())


def save_file() -> None:
    file_path = filedialog.asksaveasfilename(filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
    file = open(file_path, 'w', encoding='utf-8')
    text = text_field.get('1.0', tk.END)
    file.write(text)
    file.close()


root = tk.Tk()
root.title('Text editor')
root.geometry('600x800')

main_menu = tk.Menu(root)

file_menu = tk.Menu(main_menu, tearoff=0)
file_menu.add_command(label='Открыть', command=open_file)
file_menu.add_command(label='Сохранить', command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Закрыть', command=close_window)

view_menu = tk.Menu(main_menu, tearoff=0)
view_menu_sub = tk.Menu(view_menu, tearoff=0)
font_menu_sub = tk.Menu(view_menu, tearoff=0)
view_menu_sub.add_command(label='Тёмная', command=lambda: change_theme('dark'))
view_menu_sub.add_command(label='Светлая', command=lambda: change_theme('light'))
view_menu.add_cascade(label='Тема', menu=view_menu_sub)

font_menu_sub.add_command(label='Arial', command=lambda: change_font('Arial'))
font_menu_sub.add_command(label='Times New Roman', command=lambda: change_font('TNR'))
view_menu.add_cascade(label='Шрифт', menu=font_menu_sub)

main_menu.add_cascade(label='Файл', menu=file_menu)
main_menu.add_cascade(label='Вид', menu=view_menu)
root.config(menu=main_menu)

frame_text = tk.Frame(root)
frame_text.pack(fill=tk.BOTH, expand=1)

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

text_field = tk.Text(frame_text,
                     bg='white', fg='black',
                     padx=10, pady=10, wrap=tk.WORD,
                     insertbackground='#a5a5a5',
                     selectbackground='#3b51bf', spacing3=7,
                     width=20,
                     font='Arial 14')
text_field.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

scroll = tk.Scrollbar(frame_text, command=text_field.yview, orient=tk.VERTICAL)
scroll.pack(side=tk.LEFT, fill=tk.Y)
text_field.config(yscrollcommand=scroll.set)

root.mainloop()
