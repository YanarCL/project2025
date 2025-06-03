from tkinter import *
from PIL import Image, ImageTk

# Функция для создания полноэкранного окна
def make_fullscreen(window):
    window.attributes('-fullscreen', True)  # Открыть окно в полный экран
    window.resizable(False, False)  # Запретить изменение размера окна

# Функция для загрузки изображения
def load_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))  # Подгоняем под размер экрана
        return image
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

# Основное окно
root = Tk()
root.title('Аэрохоккей')
make_fullscreen(root)  # Делаем основное окно полноэкранным

# Загрузка изображения для главного меню
photo = load_image('D:/2 курс/Практика 2 курс 2 семестр/MainMenu.png')

if photo:
    photo = ImageTk.PhotoImage(photo)
    label = Label(root, image=photo)
    label.pack()
else:
    label = Label(root, text="Изображение не загружено", font=('Comic Sans MS', 20, 'bold'))
    label.pack()

# Функция для смены изображения
def change_image():
    new_photo = load_image('D:/2 курс/Практика 2 курс 2 семестр/Prik.png')
    if new_photo:
        new_image = ImageTk.PhotoImage(new_photo)
        label.config(image=new_image)
        label.image = new_image
        btn.place_forget()
        create_game_mode_buttons()
        exit_btn.place(relx=0.95, rely=0.95, anchor='se')
    else:
        print("Не удалось загрузить новое изображение.")

# Функция для создания кнопок режимов игры
def create_game_mode_buttons():
    global mode_buttons
    training_button = Button(root, text='ОБУЧЕНИЕ', width=35, height=1, font=('Comic Sans MS', 20, 'bold'),
                             command=open_tutorial)
    training_button.place(relx=0.5, y=100, anchor='center')
    mode_buttons.append(training_button)

    vs_computer_button = Button(root, text='ИГРА ПРОТИВ КОМПЬЮТЕРА', width=35, height=2, font=('Comic Sans MS', 20, 'bold'))
    vs_computer_button.place(relx=0.5, y=250, anchor='center')
    mode_buttons.append(vs_computer_button)

    vs_player_button = Button(root, text='ИГРА ПРОТИВ ИГРОКА', width=35, height=2, font=('Comic Sans MS', 20, 'bold'))
    vs_player_button.place(relx=0.5, y=400, anchor='center')
    mode_buttons.append(vs_player_button)

# Функция для выхода из игры
def exit_game():
    if photo:
        label.config(image=photo)
        label.image = photo
    exit_btn.place_forget()
    clear_mode_buttons()
    btn.place(relx=0.5, rely=0.5, anchor='center')

# Функция для очистки кнопок режимов игры
def clear_mode_buttons():
    global mode_buttons
    for button in mode_buttons:
        button.destroy()
    mode_buttons = []

# Функция для открытия окна обучения
def open_tutorial():
    tutorial_window = Toplevel(root)
    tutorial_window.title("Обучение")
    make_fullscreen(tutorial_window)  # Делаем окно обучения полноэкранным

    tutorial_text = """
    Добро пожаловать в обучение по игре Нонограмм!

    Цель игры:
    Заполните клеточки на поле, основываясь на числовых подсказках.
    Числа указывают, сколько клеток необходимо заполнить в строке или столбце.

    Правила:
    1. Клетки, которые необходимо заполнить, отмечаются цветом.
    2. Сначала подумайте, как лучше всего заполнить клетки, используя подсказки.
    3. Удачи в игре!

    Нажмите 'Закрыть', чтобы вернуться в игру.
    """

    label = Label(tutorial_window, text=tutorial_text, justify="left", padx=10, pady=10, font=('Arial', 10))
    label.pack()

    close_button = Button(tutorial_window, text='Закрыть', command=tutorial_window.destroy, font=('Arial', 12))
    close_button.pack(pady=10)

# Список кнопок режимов игры
mode_buttons = []

# Кнопка "Начать играть"
btn = Button(root, text='Начать играть', bg='white', fg='black', font=('Comic Sans MS', 20, 'bold'), command=change_image)
btn.place(relx=0.5, rely=0.5, anchor='center')

# Кнопка "Выход"
exit_btn = Button(root, text='Выход', bg='red', fg='white', font=('Comic Sans MS', 15), command=exit_game)
exit_btn.place_forget()

# Запуск основного цикла
root.mainloop()