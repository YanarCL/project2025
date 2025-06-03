from tkinter import *
from PIL import Image, ImageTk

# Создание основного окна
root = Tk()
root.title('Аэрохоккей')
root.attributes('-fullscreen', True)  # Открыть окно в полный экран
root.resizable(False, False)  # Запретить изменение размера окна

# Функция для загрузки изображения
def load_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))  # Подгоняем под размер экрана
        return image
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

# Загрузка изображения для главного меню
photo = load_image('D:\MainMenu.png')

if photo:
    photo = ImageTk.PhotoImage(photo)
    label = Label(root, image=photo)
    label.pack()
else:
    label = Label(root, text="Изображение не загружено", font=('Comic Sans MS', 20, 'bold'))
    label.pack()

# Функция для смены изображения
def change_image():
    new_photo = load_image('D:\FonForPlay.png')
    if new_photo:
        new_image = ImageTk.PhotoImage(new_photo)
        label.config(image=new_image)
        label.image = new_image
        btn.place_forget()
        exit_btn_main.place_forget()  # Скрываем кнопку выхода с главного экрана
        create_game_mode_buttons()
        main_menu_btn.place(relx=0.5, y=550, anchor='center')  # Размещаем кнопку "Главное меню" на том же расстоянии
    else:
        print("Не удалось загрузить новое изображение.")

# Функция для возврата в главное меню
def return_to_main_menu():
    clear_mode_buttons()  # Очищаем кнопки режимов игры
    main_menu_btn.place_forget()  # Скрываем кнопку "Главное меню"
    btn.place(relx=0.5, rely=0.5, anchor='center')  # Показываем кнопку "Начать играть"
    exit_btn_main.place(relx=0.5, rely=0.65, anchor='center')  # Показываем кнопку выхода на главном экране
    label.config(image=photo)  # Возвращаем изображение главного меню

# Функция для создания кнопок режимов игры
def create_game_mode_buttons():
    global mode_buttons
    training_button = Button(root, text='ОБУЧЕНИЕ', width=35, height=1, bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'),
                             command=open_tutorial)
    training_button.place(relx=0.5, y=100, anchor='center')
    mode_buttons.append(training_button)

    vs_computer_button = Button(root, text='ИГРА ПРОТИВ КОМПЬЮТЕРА', width=35, height=2, bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'))
    vs_computer_button.place(relx=0.5, y=250, anchor='center')
    mode_buttons.append(vs_computer_button)

    vs_player_button = Button(root, text='ИГРА ПРОТИВ ИГРОКА', width=35, height=2, bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'))
    vs_player_button.place(relx=0.5, y=400, anchor='center')
    mode_buttons.append(vs_player_button)

# Функция для выхода из игры
def exit_game():
    root.destroy()  # Закрыть приложение

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
    tutorial_window.geometry('1000x300')  # Фиксированный размер окна обучения
    tutorial_window.resizable(False, False)  # Запретить изменение размера окна

    tutorial_text = """
    Добро пожаловать в обучение по игре Аэрохоккей!

    Цель: забить как можно больше шайб в ворота соперника и не дать ему забить в собственные.
Игровой процесс: в начале игры шайба появляется на середине поля, и соперники могут двигаться только на своей половине с помощью WASD или стрелок.
Любая из сторон может двигать свою биту в середину и отбить шайбу в сторону противника. 
После забитой шайбы в одни из ворот она автоматически вновь появляется на середине, а счет увеличивается на единицу


    Закройте окно, чтобы вернуться в игру.
    """

    label = Label(tutorial_window, text=tutorial_text, justify="left", padx=10, pady=10, font=('Arial', 10))
    label.pack()

    close_button = Button(tutorial_window, text='Закрыть', command=tutorial_window.destroy, font=('Arial', 12))
    close_button.pack(pady=10)

# Список кнопок режимов игры
mode_buttons = []

# Кнопка "Начать играть"
btn = Button(root, text='Начать играть', width=35, height=2, bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'), command=change_image)
btn.place(relx=0.5, rely=0.5, anchor='center')

# Кнопка "Выход" на главном экране
exit_btn_main = Button(root, text='Выход', width=35, height=2, bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'), command=exit_game)
exit_btn_main.place(relx=0.5, rely=0.65, anchor='center')  # Размещаем кнопку выхода под кнопкой "Начать играть"

# Кнопка "Главное меню" для второго экрана
main_menu_btn = Button(root, text='Главное меню', width=35, height=2, bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'), command=return_to_main_menu)
main_menu_btn.place_forget()  # Скрываем кнопку "Главное меню" на старте

# Запуск основного цикла
root.mainloop()