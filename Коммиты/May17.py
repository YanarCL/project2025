from tkinter import *
from PIL import Image, ImageTk
import math
import random

# Создание основного окна
root = Tk()
root.title('Аэрохоккей')
root.attributes('-fullscreen', True)
root.resizable(False, False)

# Функция для загрузки изображения
def load_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        return image
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

# Загрузка изображений
main_menu_image = load_image('images/MainMenu.png')
mode_select_image = load_image('images/FonForPlay.png')

# Создание фонового изображения для главного меню
if main_menu_image:
    main_menu_photo = ImageTk.PhotoImage(main_menu_image)
    label = Label(root, image=main_menu_photo)
    label.pack()
else:
    label = Label(root, text="Изображение не загружено", font=('Arial', 20, 'bold'))
    label.pack()

# Настройки игры (изменяемые параметры)
game_settings = {
    'PADDLE_SPEED': 8,
    'BALL_SPEED': 12,
    'WIN_SCORE': 4
}

# Константы
WIDTH = 1000
HEIGHT = 500
PADDLE_RADIUS = 30
BALL_RADIUS = 15
COMPUTER_REACTION = 0.7  # Коэффициент реакции компьютера (0-1)

# Глобальные переменные
mode_buttons = []
bg_label = None
canvas = None
tutorial_window = None
settings_window = None
score_a = 0
score_b = 0
ball_speed_x = 0
ball_speed_y = 0
ball_is_moving = False
is_paused = False
game_over = False
game_mode = None  # 'player_vs_player' или 'player_vs_computer'
player_started_moving = False  # Флаг, что игрок начал движение
keys_pressed = {
    87: False, 65: False, 83: False, 68: False,  # WASD
    38: False, 40: False, 37: False, 39: False,   # Стрелки
    32: False                                    # Пробел
}

# Функция для смены изображения на экран выбора режима
def change_image():
    if mode_select_image:
        new_image = ImageTk.PhotoImage(mode_select_image)
        label.config(image=new_image)
        label.image = new_image
        btn.place_forget()
        settings_btn.place_forget()
        exit_btn_main.place_forget()
        create_game_mode_buttons()
        main_menu_btn.place(relx=0.5, y=550, anchor='center')

# Функция для возврата в главное меню
def return_to_main_menu():
    clear_mode_buttons()
    main_menu_btn.place_forget()
    btn.place(relx=0.5, rely=0.5, anchor='center')
    settings_btn.place(relx=0.5, rely=0.65, anchor='center')
    exit_btn_main.place(relx=0.5, rely=0.8, anchor='center')
    label.config(image=main_menu_photo)
    label.pack()

# Функция для создания кнопок режимов игры
def create_game_mode_buttons():
    global mode_buttons
    
    training_button = Button(root, text='ОБУЧЕНИЕ', width=35, height=1, bg='#080675', 
                           fg='#AFD7FF', font=('impact', 20, 'bold'), command=open_tutorial)
    training_button.place(relx=0.5, y=100, anchor='center')
    mode_buttons.append(training_button)

    vs_computer_button = Button(root, text='ИГРА ПРОТИВ КОМПЬЮТЕРА', width=35, height=2, 
                              bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'),
                              command=start_vs_computer_game)
    vs_computer_button.place(relx=0.5, y=250, anchor='center')
    mode_buttons.append(vs_computer_button)

    vs_player_button = Button(root, text='ИГРА ПРОТИВ ИГРОКА', width=35, height=2, 
                            bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'),
                            command=start_vs_player_game)
    vs_player_button.place(relx=0.5, y=400, anchor='center')
    mode_buttons.append(vs_player_button)

# Функция для очистки кнопок режимов игры
def clear_mode_buttons():
    global mode_buttons
    for button in mode_buttons:
        button.destroy()
    mode_buttons = []

# Функция для открытия обучения
def open_tutorial():
    global tutorial_window
    
    # Если окно уже существует и не уничтожено
    if tutorial_window is not None and tutorial_window.winfo_exists():
        # Перемещаем фокус на существующее окно
        tutorial_window.lift()
        return
    
    tutorial_window = Toplevel(root)
    tutorial_window.title("Обучение")
    tutorial_window.geometry('1000x300')
    tutorial_window.resizable(False, False)
    
    # Центрирование окна обучения
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1000) // 2
    y = (screen_height - 300) // 2
    tutorial_window.geometry(f'1000x300+{x}+{y}')
    
    # Обработчик закрытия окна
    tutorial_window.protocol("WM_DELETE_WINDOW", close_tutorial)

    tutorial_text = """
    Игровой процесс: в начале игры шайба появляется на середине поля, и соперники могут двигаться только на своей половине с помощью WASD или стрелок.
Любая из сторон может двигать свою биту в середину и отбить шайбу в сторону противника. 
После забитой шайбы в одни из ворот она автоматически вновь появляется на середине, а счет увеличивается на единицу

    Цель: забить как можно больше шайб в ворота соперника.
    Управление:
      В игре против компьютера:
    - Игрок (синий): WASD или Стрелки
    - Пробел: Пауза
      В игре против игрока:
    - Игрок (синий): WASD
    - игрок (красный): Стрелки
    """
    Label(tutorial_window, text=tutorial_text, justify="left", padx=10, pady=10, 
         font=('Arial', 10)).pack()
    Button(tutorial_window, text='Закрыть', command=close_tutorial, 
          font=('Arial', 12)).pack(pady=10)

def close_tutorial():
    global tutorial_window
    if tutorial_window is not None:
        tutorial_window.destroy()
        tutorial_window = None

# Функция для открытия настроек
def open_settings():
    global settings_window
    
    # Если окно уже существует и не уничтожено
    if settings_window is not None and settings_window.winfo_exists():
        # Перемещаем фокус на существующее окно
        settings_window.lift()
        return
    
    settings_window = Toplevel(root)
    settings_window.title("Настройки")
    settings_window.geometry('400x400')
    settings_window.resizable(False, False)
    
    # Центрирование окна настроек
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 400) // 2
    settings_window.geometry(f'400x400+{x}+{y}')
    
    # Обработчик закрытия окна
    settings_window.protocol("WM_DELETE_WINDOW", close_settings)
    
    # Создание элементов интерфейса
    Label(settings_window, text="Настройки игры", font=('Arial', 20, 'bold')).pack(pady=10)
    
    # Очки для победы (1-20)
    Label(settings_window, text="Очки для победы (1-20):", font=('Arial', 12)).pack(pady=5)
    win_score_entry = Entry(settings_window, font=('Arial', 12), justify='center')
    win_score_entry.insert(0, str(game_settings['WIN_SCORE']))
    win_score_entry.pack(pady=5)
    
    # Скорость бит (1-20)
    Label(settings_window, text="Скорость бит (1-20):", font=('Arial', 12)).pack(pady=5)
    paddle_speed_entry = Entry(settings_window, font=('Arial', 12), justify='center')
    paddle_speed_entry.insert(0, str(game_settings['PADDLE_SPEED']))
    paddle_speed_entry.pack(pady=5)
    
    # Скорость шайбы (1-20)
    Label(settings_window, text="Скорость шайбы (1-20):", font=('Arial', 12)).pack(pady=5)
    ball_speed_entry = Entry(settings_window, font=('Arial', 12), justify='center')
    ball_speed_entry.insert(0, str(game_settings['BALL_SPEED']))
    ball_speed_entry.pack(pady=5)
    
    # Функция сохранения настроек
    def save_settings():
        try:
            # Получаем и ограничиваем значения
            win_score = int(win_score_entry.get())
            paddle_speed = int(paddle_speed_entry.get())
            ball_speed = int(ball_speed_entry.get())
            
            # Применяем ограничения
            game_settings['WIN_SCORE'] = max(1, min(20, win_score))
            game_settings['PADDLE_SPEED'] = max(1, min(20, paddle_speed))
            game_settings['BALL_SPEED'] = max(1, min(20, ball_speed))
            
            # Обновляем поля ввода актуальными значениями
            win_score_entry.delete(0, END)
            win_score_entry.insert(0, str(game_settings['WIN_SCORE']))
            paddle_speed_entry.delete(0, END)
            paddle_speed_entry.insert(0, str(game_settings['PADDLE_SPEED']))
            ball_speed_entry.delete(0, END)
            ball_speed_entry.insert(0, str(game_settings['BALL_SPEED']))
            
            # Показываем сообщение об успешном сохранении
            success_label = Label(settings_window, text="Настройки сохранены!", fg='green')
            success_label.pack()
            settings_window.after(1000, success_label.destroy)
            
        except ValueError:
            error_label = Label(settings_window, text="Введите целые числа от 1 до 20!", fg='red')
            error_label.pack()
            settings_window.after(2000, error_label.destroy)
    
    # Кнопки
    Button(settings_window, text="Сохранить", font=('Arial', 12), 
          command=save_settings).pack(pady=10)
    Button(settings_window, text="Вернуться", font=('Arial', 12), 
          command=close_settings).pack(pady=10)

def close_settings():
    global settings_window
    if settings_window is not None:
        settings_window.destroy()
        settings_window = None

# Функция для выхода из игры
def exit_game():
    root.destroy()

# Функция запуска игры против компьютера
def start_vs_computer_game():
    global bg_label, canvas, score_a, score_b, ball_speed_x, ball_speed_y, ball_is_moving, is_paused, game_over, game_mode, player_started_moving
    
    # Устанавливаем режим игры
    game_mode = 'player_vs_computer'
    player_started_moving = False
    
    score_a = 0
    score_b = 0
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False
    is_paused = False
    game_over = False
    
    label.pack_forget()
    for button in mode_buttons:
        button.place_forget()
    main_menu_btn.place_forget()
    
    if mode_select_image:
        bg_image = ImageTk.PhotoImage(mode_select_image)
        bg_label = Label(root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
   
    game_background = load_image("images\GameFone.png")
    if game_background:
        game_background = game_background.resize((WIDTH, HEIGHT))
        game_background = ImageTk.PhotoImage(game_background)
        canvas.create_image(0, 0, anchor=NW, image=game_background, tags="background")
        canvas.image = game_background
    
    # Инициализация игры
    init_game()
    reset_ball()
    
    # Создаем меню паузы
    create_pause_menu()
    
    # Привязка клавиш
    root.bind("<KeyPress>", key_pressed)
    root.bind("<KeyRelease>", key_released)
    
    # Запуск игрового цикла
    update_ball()
    move_paddles()

# Функция запуска игры против игрока
def start_vs_player_game():
    global bg_label, canvas, score_a, score_b, ball_speed_x, ball_speed_y, ball_is_moving, is_paused, game_over, game_mode, player_started_moving
   
    game_mode = 'player_vs_player'
    player_started_moving = False
    
    score_a = 0
    score_b = 0
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False
    is_paused = False
    game_over = False
    label.pack_forget()
    for button in mode_buttons:
        button.place_forget()
    main_menu_btn.place_forget()
    
    if mode_select_image:
        bg_image = ImageTk.PhotoImage(mode_select_image)
        bg_label = Label(root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    game_background = load_image("images/GameFone.png")
    if game_background:
        game_background = game_background.resize((WIDTH, HEIGHT))
        game_background = ImageTk.PhotoImage(game_background)
        canvas.create_image(0, 0, anchor=NW, image=game_background, tags="background")
        canvas.image = game_background
    
    init_game()
    reset_ball()

    create_pause_menu()

    root.bind("<KeyPress>", key_pressed)
    root.bind("<KeyRelease>", key_released)
    
    # Запуск игрового цикла
    update_ball()
    move_paddles()

# Инициализация игровых элементов
def init_game():
    global paddle_a, paddle_b, ball, score_text
    
    # Создаем текст счета
    score_text = canvas.create_text(WIDTH // 2, 30, 
                                 text=f"Синий: {score_a}  Красный: {score_b}", 
                                 font=("Arial", 30), fill="black")

    # Создаем биты игроков
    paddle_a = canvas.create_oval(
        WIDTH // 4 - PADDLE_RADIUS, HEIGHT // 2 - PADDLE_RADIUS,
        WIDTH // 4 + PADDLE_RADIUS, HEIGHT // 2 + PADDLE_RADIUS,
        fill="blue", outline="black"
    )

    paddle_b = canvas.create_oval(
        3 * WIDTH // 4 - PADDLE_RADIUS, HEIGHT // 2 - PADDLE_RADIUS,
        3 * WIDTH // 4 + PADDLE_RADIUS, HEIGHT // 2 + PADDLE_RADIUS,
        fill="red", outline="black"
    )

    # Создаем шайбу
    ball = canvas.create_oval(
        WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS,
        WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS,
        fill="white", outline="black"
    )

    # Рисуем ворота и разметку
    goal_width = 200
    canvas.create_rectangle(0, HEIGHT // 2 - goal_width // 2, 10, HEIGHT // 2 + goal_width // 2, 
                          fill="gray", outline="black")
    canvas.create_rectangle(WIDTH - 10, HEIGHT // 2 - goal_width // 2, WIDTH, HEIGHT // 2 + goal_width // 2, 
                          fill="gray", outline="black")
    canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill="gray", dash=(5, 5))
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, outline="white", width=3)

# Создание меню паузы
def create_pause_menu():
    global pause_menu
    pause_menu = Frame(root, bg="black", padx=40, pady=30)
    Label(pause_menu, text="ПАУЗА", font=("Arial", 36, 'bold'), bg="black", fg="white").pack(pady=15)
    Button(pause_menu, text="Продолжить", font=("Arial", 24), 
          command=toggle_pause, bg="#333", fg="white", width=15).pack(pady=10)
    Button(pause_menu, text="Заново", font=("Arial", 24), 
          command=restart_game, bg="#333", fg="white", width=15).pack(pady=10)
    Button(pause_menu, text="Выход", font=("Arial", 24), 
          command=return_to_game_menu, bg="#333", fg="white", width=15).pack(pady=10)
    pause_menu.place(relx=0.5, rely=0.5, anchor=CENTER)
    pause_menu.place_forget()

# Перезапуск игры
def restart_game():
    global score_a, score_b, ball_speed_x, ball_speed_y, ball_is_moving, is_paused, game_over, player_started_moving
    
    # Сброс состояния игры
    is_paused = False
    game_over = False
    score_a = 0
    score_b = 0
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False
    player_started_moving = False
    
    # Удаляем только игровые элементы
    items = canvas.find_all()
    for item in items:
        if "background" not in canvas.gettags(item):
            canvas.delete(item)
    
    # Переинициализация игры
    init_game()
    reset_ball()
    hide_pause_menu()

# Обработчики клавиш
def key_pressed(event):
    global keys_pressed, player_started_moving
    
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = True
        # Отмечаем, что игрок начал движение (актуально для игры против компьютера)
        if game_mode == 'player_vs_computer' and not player_started_moving:
            if event.keycode in [87, 65, 83, 68, 38, 40, 37, 39]:  # WASD или стрелки
                player_started_moving = True
            
    if event.keycode == 32:  # Пробел
        toggle_pause()

def key_released(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = False

# Управление паузой
def toggle_pause():
    global is_paused
    if not game_over:
        is_paused = not is_paused
        if is_paused:
            show_pause_menu()
        else:
            hide_pause_menu()

def show_pause_menu():
    pause_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

def hide_pause_menu():
    pause_menu.place_forget()

# Движение бит
def move_paddles():
    if not is_paused and not game_over:
        # Движение биты игрока (WASD или стрелки)
        x1, y1, x2, y2 = canvas.coords(paddle_a)
        
        # Управление WASD
        if keys_pressed[87] and y1 > 0:  # W
            canvas.move(paddle_a, 0, -game_settings['PADDLE_SPEED'])
        if keys_pressed[83] and y2 < HEIGHT:  # S
            canvas.move(paddle_a, 0, game_settings['PADDLE_SPEED'])
        if keys_pressed[65] and x1 > 0:  # A
            canvas.move(paddle_a, -game_settings['PADDLE_SPEED'], 0)
        if keys_pressed[68] and x2 < WIDTH // 2:  # D
            canvas.move(paddle_a, game_settings['PADDLE_SPEED'], 0)
            
        # Управление стрелками (только в режиме против компьютера)
        if game_mode == 'player_vs_computer':
            if keys_pressed[38] and y1 > 0:  # Стрелка вверх
                canvas.move(paddle_a, 0, -game_settings['PADDLE_SPEED'])
            if keys_pressed[40] and y2 < HEIGHT:  # Стрелка вниз
                canvas.move(paddle_a, 0, game_settings['PADDLE_SPEED'])
            if keys_pressed[37] and x1 > 0:  # Стрелка влево
                canvas.move(paddle_a, -game_settings['PADDLE_SPEED'], 0)
            if keys_pressed[39] and x2 < WIDTH // 2:  # Стрелка вправо
                canvas.move(paddle_a, game_settings['PADDLE_SPEED'], 0)

        # Движение биты компьютера или второго игрока
        if game_mode == 'player_vs_player':
            # Управление вторым игроком (стрелки)
            x1, y1, x2, y2 = canvas.coords(paddle_b)
            if keys_pressed[38] and y1 > 0:  # Стрелка вверх
                canvas.move(paddle_b, 0, -game_settings['PADDLE_SPEED'])
            if keys_pressed[40] and y2 < HEIGHT:  # Стрелка вниз
                canvas.move(paddle_b, 0, game_settings['PADDLE_SPEED'])
            if keys_pressed[37] and x1 > WIDTH // 2:  # Стрелка влево
                canvas.move(paddle_b, -game_settings['PADDLE_SPEED'], 0)
            if keys_pressed[39] and x2 < WIDTH:  # Стрелка вправо
                canvas.move(paddle_b, game_settings['PADDLE_SPEED'], 0)
        elif player_started_moving:  # Игра против компьютера
            move_computer_paddle()

        check_ball_collision()

    root.after(20, move_paddles)

# ИИ компьютера
def move_computer_paddle():
    ball_coords = canvas.coords(ball)
    paddle_coords = canvas.coords(paddle_b)
    
    ball_center_y = (ball_coords[1] + ball_coords[3]) / 2
    paddle_center_y = (paddle_coords[1] + paddle_coords[3]) / 2
    paddle_center_x = (paddle_coords[0] + paddle_coords[2]) / 2
    
    # Если шайба двигается, компьютер реагирует
    if ball_is_moving:
        # Вычисляем предполагаемую точку пересечения с линией компьютера
        if ball_speed_x > 0:  # Шайба движется вправо (к компьютеру)
            if ball_speed_y != 0:
                time_to_reach = (paddle_center_x - (ball_coords[0] + ball_coords[2]) / 2) / ball_speed_x
                predicted_y = ball_center_y + ball_speed_y * time_to_reach
                
                # Ограничиваем предсказанную позицию в пределах поля
                predicted_y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, predicted_y))
                
                # Двигаемся к предсказанной позиции с учетом коэффициента реакции
                if paddle_center_y < predicted_y - 10 * COMPUTER_REACTION:
                    canvas.move(paddle_b, 0, game_settings['PADDLE_SPEED'] * COMPUTER_REACTION)
                elif paddle_center_y > predicted_y + 10 * COMPUTER_REACTION:
                    canvas.move(paddle_b, 0, -game_settings['PADDLE_SPEED'] * COMPUTER_REACTION)
            else:
                # Если шайба движется прямо, просто следуем за ней по Y
                if paddle_center_y < ball_center_y - 10 * COMPUTER_REACTION:
                    canvas.move(paddle_b, 0, game_settings['PADDLE_SPEED'] * COMPUTER_REACTION)
                elif paddle_center_y > ball_center_y + 10 * COMPUTER_REACTION:
                    canvas.move(paddle_b, 0, -game_settings['PADDLE_SPEED'] * COMPUTER_REACTION)
        else:
            # Если шайба движется от компьютера, возвращаемся в центр
            center_y = HEIGHT / 2
            if paddle_center_y < center_y - 10:
                canvas.move(paddle_b, 0, game_settings['PADDLE_SPEED'] * COMPUTER_REACTION * 0.5)
            elif paddle_center_y > center_y + 10:
                canvas.move(paddle_b, 0, -game_settings['PADDLE_SPEED'] * COMPUTER_REACTION * 0.5)
    else:
        # Если шайба не двигается, компьютер ждет в центре
        center_y = HEIGHT / 2
        if paddle_center_y < center_y - 10:
            canvas.move(paddle_b, 0, game_settings['PADDLE_SPEED'] * 0.5)
        elif paddle_center_y > center_y + 10:
            canvas.move(paddle_b, 0, -game_settings['PADDLE_SPEED'] * 0.5)
    
    # Проверяем границы поля для компьютера
    x1, y1, x2, y2 = canvas.coords(paddle_b)
    if y1 < 0:
        canvas.move(paddle_b, 0, -y1)
    if y2 > HEIGHT:
        canvas.move(paddle_b, 0, HEIGHT - y2)
    if x1 < WIDTH // 2:
        canvas.move(paddle_b, WIDTH // 2 - x1, 0)
    if x2 > WIDTH:
        canvas.move(paddle_b, WIDTH - x2, 0)

# Проверка столкновений
def check_ball_collision():
    global ball_speed_x, ball_speed_y, ball_is_moving

    ball_coords = canvas.coords(ball)
    paddle_a_coords = canvas.coords(paddle_a)
    paddle_b_coords = canvas.coords(paddle_b)

    # Столкновение с битой A
    if (ball_coords[0] <= paddle_a_coords[2] and ball_coords[2] >= paddle_a_coords[0] and
        ball_coords[1] <= paddle_a_coords[3] and ball_coords[3] >= paddle_a_coords[1]):
        if ball_is_moving:
            handle_collision(paddle_a_coords, ball_coords)
        elif (keys_pressed[87] or keys_pressed[83] or keys_pressed[65] or keys_pressed[68] or 
              (game_mode == 'player_vs_computer' and 
               (keys_pressed[38] or keys_pressed[40] or keys_pressed[37] or keys_pressed[39]))):
            start_ball_movement(paddle_a_coords, ball_coords)

    # Столкновение с битой B
    if (ball_coords[0] <= paddle_b_coords[2] and ball_coords[2] >= paddle_b_coords[0] and
        ball_coords[1] <= paddle_b_coords[3] and ball_coords[3] >= paddle_b_coords[1]):
        if ball_is_moving:
            handle_collision(paddle_b_coords, ball_coords)
        elif game_mode == 'player_vs_player' and (keys_pressed[38] or keys_pressed[40] or keys_pressed[37] or keys_pressed[39]):
            start_ball_movement(paddle_b_coords, ball_coords)
        elif game_mode == 'player_vs_computer' and player_started_moving:
            start_ball_movement(paddle_b_coords, ball_coords)

    # Столкновение с задней стенкой
    if ball_is_moving:
        x1, y1, x2, y2 = ball_coords
        if x1 <= 0 or x2 >= WIDTH:
            # Проверяем, не попала ли шайба в ворота
            goal_top = HEIGHT // 2 - 100
            goal_bottom = HEIGHT // 2 + 100
            if not (y1 >= goal_top and y2 <= goal_bottom):
                # Если не в воротах, отскакиваем от стенки
                ball_speed_x *= -1
                # Слегка корректируем позицию, чтобы избежать залипания
                if x1 <= 0:
                    canvas.move(ball, 5, 0)
                else:
                    canvas.move(ball, -5, 0)
                
                # Добавляем небольшой случайный угол при отскоке от стенки
                ball_speed_y += random.uniform(-1, 1)
                # Нормализуем скорость
                speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2)
                if speed > 0:
                    ball_speed_x = (ball_speed_x / speed) * game_settings['BALL_SPEED']
                    ball_speed_y = (ball_speed_y / speed) * game_settings['BALL_SPEED']

def start_ball_movement(paddle_coords, ball_coords):
    global ball_speed_x, ball_speed_y, ball_is_moving
    
    paddle_center_x = (paddle_coords[0] + paddle_coords[2]) / 2
    paddle_center_y = (paddle_coords[1] + paddle_coords[3]) / 2
    ball_center_x = (ball_coords[0] + ball_coords[2]) / 2
    ball_center_y = (ball_coords[1] + ball_coords[3]) / 2

    # Определяем направление от биты к центру поля
    if paddle_center_x < WIDTH / 2:  # Левая бита
        direction_x = 1  # Вправо
    else:  # Правая бита
        direction_x = -1  # Влево
    
    # Добавляем небольшое вертикальное движение в зависимости от положения шайбы относительно биты
    direction_y = (ball_center_y - paddle_center_y) / PADDLE_RADIUS
    
    # Нормализуем вектор направления
    length = math.sqrt(direction_x**2 + direction_y**2)
    if length > 0:
        direction_x /= length
        direction_y /= length
    
    # Устанавливаем скорость шайбы равной текущей настройке BALL_SPEED
    ball_speed_x = game_settings['BALL_SPEED'] * direction_x
    ball_speed_y = game_settings['BALL_SPEED'] * direction_y
    ball_is_moving = True

def handle_collision(paddle_coords, ball_coords):
    global ball_speed_x, ball_speed_y
    
    paddle_center_x = (paddle_coords[0] + paddle_coords[2]) / 2
    paddle_center_y = (paddle_coords[1] + paddle_coords[3]) / 2
    ball_center_x = (ball_coords[0] + ball_coords[2]) / 2
    ball_center_y = (ball_coords[1] + ball_coords[3]) / 2

    dx = ball_center_x - paddle_center_x
    dy = ball_center_y - paddle_center_y

    length = max(math.sqrt(dx**2 + dy**2), 0.1)
    dx /= length
    dy /= length

    # Устанавливаем скорость шайбы равной текущей настройке BALL_SPEED после столкновения
    ball_speed_x = game_settings['BALL_SPEED'] * dx
    ball_speed_y = game_settings['BALL_SPEED'] * dy

    # Добавляем небольшой случайный угол при столкновении
    ball_speed_y += random.uniform(-0.5, 0.5)
    
    # Нормализуем скорость
    speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2)
    if speed > 0:
        ball_speed_x = (ball_speed_x / speed) * game_settings['BALL_SPEED']
        ball_speed_y = (ball_speed_y / speed) * game_settings['BALL_SPEED']

    overlap = PADDLE_RADIUS + BALL_RADIUS - length + 5
    canvas.move(ball, dx * overlap, dy * overlap)

# Обновление положения шайбы
def update_ball():
    global ball_speed_x, ball_speed_y, score_a, score_b, game_over
    
    if is_paused or game_over:
        root.after(20, update_ball)
        return
    
    if ball_is_moving:
        # Получаем текущие координаты шайбы
        x1, y1, x2, y2 = canvas.coords(ball)
        
        # Проверяем выход за границы поля по Y
        if y1 < 0:
            y1 = 0
            y2 = y1 + 2 * BALL_RADIUS
            ball_speed_y *= -1
        if y2 > HEIGHT:
            y2 = HEIGHT
            y1 = y2 - 2 * BALL_RADIUS
            ball_speed_y *= -1
            
        canvas.coords(ball, x1, y1, x2, y2)
        
        # Проверка голов
        goal_width = 200
        goal_top = HEIGHT // 2 - goal_width // 2
        goal_bottom = HEIGHT // 2 + goal_width // 2
        
        if x1 <= 10 and y1 >= goal_top and y2 <= goal_bottom:
            score_b += 1
            reset_ball()
        elif x2 >= WIDTH - 10 and y1 >= goal_top and y2 <= goal_bottom:
            score_a += 1
            reset_ball()
        else:
            canvas.move(ball, ball_speed_x, ball_speed_y)

        # Обновляем счет
        canvas.itemconfig(score_text, text=f"Синий: {score_a}  Красный: {score_b}")

        if score_a >= game_settings['WIN_SCORE'] or score_b >= game_settings['WIN_SCORE']:
            end_game()
    
    root.after(20, update_ball)

# Сброс шайбы в центр
def reset_ball():
    global ball_speed_x, ball_speed_y, ball_is_moving, player_started_moving
    
    canvas.coords(ball, 
                 WIDTH // 2 - BALL_RADIUS, 
                 HEIGHT // 2 - BALL_RADIUS, 
                 WIDTH // 2 + BALL_RADIUS, 
                 HEIGHT // 2 + BALL_RADIUS)
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False
    # В режиме против компьютера сбрасываем флаг начала движения
    if game_mode == 'player_vs_computer':
        player_started_moving = False

# Окончание игры
def end_game():
    global game_over, end_menu
    
    game_over = True
    winner = "Синий игрок" if score_a >= game_settings['WIN_SCORE'] else "Красный игрок"
    
    end_menu = Frame(root, bg="black", padx=40, pady=30)
    Label(end_menu, text=f"{winner} победил!", font=("Arial", 36, 'bold'), 
         bg="black", fg="white").pack(pady=15)
    
    Button(end_menu, text="Заново", font=("Arial", 24), 
          command=lambda: [end_menu.destroy(), restart_game()], 
          bg="#333", fg="white", width=15).pack(pady=10)
    Button(end_menu, text="Выход", font=("Arial", 24), 
          command=lambda: [end_menu.destroy(), return_to_game_menu()], 
          bg="#333", fg="white", width=15).pack(pady=10)
    
    end_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

# Возврат в меню выбора режима
def return_to_game_menu():
    global is_paused, game_over, player_started_moving
    
    is_paused = False
    game_over = False
    player_started_moving = False
    
    hide_pause_menu()
    if 'end_menu' in globals():
        end_menu.destroy()
    
    canvas.destroy()
    bg_label.destroy()
    
    root.unbind("<KeyPress>")
    root.unbind("<KeyRelease>")
    
    clear_mode_buttons()
    create_game_mode_buttons()
    main_menu_btn.place(relx=0.5, y=550, anchor='center')
    
    if mode_select_image:
        new_image = ImageTk.PhotoImage(mode_select_image)
        label.config(image=new_image)
        label.image = new_image
        label.pack()

# Создание кнопок интерфейса
btn = Button(root, text='Начать играть', width=35, height=2, 
            bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'), 
            command=change_image)
btn.place(relx=0.5, rely=0.5, anchor='center')

settings_btn = Button(root, text='Настройки', width=35, height=2,
                     bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'),
                     command=open_settings)
settings_btn.place(relx=0.5, rely=0.65, anchor='center')

exit_btn_main = Button(root, text='Выход', width=35, height=2, 
                      bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'), 
                      command=exit_game)
exit_btn_main.place(relx=0.5, rely=0.8, anchor='center')

main_menu_btn = Button(root, text='Главное меню', width=35, height=2, 
                      bg='#080675', fg='#AFD7FF', font=('impact', 20, 'bold'), 
                      command=return_to_main_menu)
main_menu_btn.place_forget()

# Запуск основного цикла
root.mainloop()