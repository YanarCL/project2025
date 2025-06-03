from tkinter import *
from PIL import Image, ImageTk
import math

# Создание основного окна
root = Tk()
root.title('Аэрохоккей')
root.attributes('-fullscreen', True)  # Открыть окно в полный экран
root.resizable(False, False)  # Запретить изменение размера окна

# Константы игры
WIDTH = 1000
HEIGHT = 500
PADDLE_RADIUS = 30
BALL_RADIUS = 15
PADDLE_SPEED = 8
BALL_SPEED = 14
WIN_SCORE = 4

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
        exit_btn_main.place_forget()
        create_game_mode_buttons()
        main_menu_btn.place(relx=0.5, y=550, anchor='center')
    else:
        print("Не удалось загрузить новое изображение.")

def return_to_main_menu():
    if 'canvas' in globals():
        canvas.destroy()
        root.unbind("<KeyPress>")
        root.unbind("<KeyRelease>")
    
    clear_mode_buttons()
    main_menu_btn.place_forget()
    btn.place(relx=0.5, rely=0.5, anchor='center')
    exit_btn_main.place(relx=0.5, rely=0.65, anchor='center')
    label.config(image=photo)
    label.pack()

def create_game_mode_buttons():
    global mode_buttons
    training_button = Button(root, text='ОБУЧЕНИЕ', width=35, height=1, bg='#080675', fg='#AFD7FF', 
                           font=('impact', 20, 'bold'), command=open_tutorial)
    training_button.place(relx=0.5, y=100, anchor='center')
    mode_buttons.append(training_button)

    vs_computer_button = Button(root, text='ИГРА ПРОТИВ КОМПЬЮТЕРА', width=35, height=2, bg='#080675', 
                              fg='#AFD7FF', font=('impact', 20, 'bold'), command=start_vs_computer_game)
    vs_computer_button.place(relx=0.5, y=250, anchor='center')
    mode_buttons.append(vs_computer_button)

    vs_player_button = Button(root, text='ИГРА ПРОТИВ ИГРОКА', width=35, height=2, bg='#080675', 
                            fg='#AFD7FF', font=('impact', 20, 'bold'), command=start_vs_player_game)
    vs_player_button.place(relx=0.5, y=400, anchor='center')
    mode_buttons.append(vs_player_button)

def exit_game():
    root.destroy()

def clear_mode_buttons():
    global mode_buttons
    for button in mode_buttons:
        button.destroy()
    mode_buttons = []

def open_tutorial():
    tutorial_window = Toplevel(root)
    tutorial_window.title("Обучение")
    tutorial_window.geometry('1000x300')
    tutorial_window.resizable(False, False)

    tutorial_text = """
    Добро пожаловать в обучение по игре Аэрохоккей!

    Управление:
    - Игрок 1 (синий): WASD
    - Игрок 2 (красный): Стрелки
    - Пробел: Пауза

    Цель: забить шайбу в ворота соперника.
    После гола шайба возвращается в центр.
    Игра идет до 4 очков.
    """
    
    Label(tutorial_window, text=tutorial_text, justify="left", padx=10, pady=10, 
          font=('Arial', 12)).pack()
    Button(tutorial_window, text='Закрыть', command=tutorial_window.destroy, 
           font=('Arial', 12)).pack(pady=10)

# Игровая логика
def start_vs_player_game():
    global canvas, score_a, score_b, score_text, paddle_a, paddle_b, ball
    global ball_speed_x, ball_speed_y, ball_is_moving, is_paused, game_over, keys_pressed
    
    # Скрытие меню
    label.pack_forget()
    for button in mode_buttons:
        button.place_forget()
    main_menu_btn.place_forget()
    
    # Инициализация игры
    score_a = 0
    score_b = 0
    ball_is_moving = False
    is_paused = False
    game_over = False
    
    keys_pressed = {
        87: False, 65: False, 83: False, 68: False,  # WASD
        38: False, 40: False, 37: False, 39: False,   # Стрелки
        32: False                                    # Пробел
    }
    
    # Создание игрового поля
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Фон игры
    game_bg = load_image("D:\GameFone.png")
    if game_bg:
        game_bg = game_bg.resize((WIDTH, HEIGHT))
        game_bg = ImageTk.PhotoImage(game_bg)
        canvas.create_image(0, 0, anchor=NW, image=game_bg, tags="background")
        canvas.image = game_bg
    
    # Игровые элементы
    init_game()
    reset_ball()
    
    # Меню паузы
    create_pause_menu()
    
    # Привязка клавиш
    root.bind("<KeyPress>", key_pressed)
    root.bind("<KeyRelease>", key_released)
    
    # Запуск игрового цикла
    update_ball()
    move_paddles()

def start_vs_computer_game():
    # Аналогично start_vs_player_game, но с ИИ для компьютера
    start_vs_player_game()  # Временно используем тот же код

def create_pause_menu():
    global pause_menu
    pause_menu = Frame(root, bg="black", padx=40, pady=30)
    Label(pause_menu, text="ПАУЗА", font=("Arial", 36, 'bold'), 
          bg="black", fg="white").pack(pady=15)
    Button(pause_menu, text="Продолжить", font=("Arial", 24), 
           command=toggle_pause, bg="#333", fg="white", width=15).pack(pady=10)
    Button(pause_menu, text="Заново", font=("Arial", 24), 
           command=restart_game, bg="#333", fg="white", width=15).pack(pady=10)
    Button(pause_menu, text="В главное меню", font=("Arial", 24), 
           command=return_to_game_menu, bg="#333", fg="white", width=15).pack(pady=10)
    pause_menu.place(relx=0.5, rely=0.5, anchor=CENTER)
    pause_menu.place_forget()

def return_to_game_menu():
    hide_pause_menu()
    if 'end_menu' in globals():
        end_menu.destroy()
    canvas.destroy()
    root.unbind("<KeyPress>")
    root.unbind("<KeyRelease>")
    return_to_main_menu()

def init_game():
    global paddle_a, paddle_b, ball, score_text
    
    # Счет
    score_text = canvas.create_text(WIDTH//2, 30, 
                                  text=f"Синий: {score_a}  Красный: {score_b}", 
                                  font=("Arial", 30), fill="white")
    
    # Биты игроков
    paddle_a = canvas.create_oval(
        WIDTH//4 - PADDLE_RADIUS, HEIGHT//2 - PADDLE_RADIUS,
        WIDTH//4 + PADDLE_RADIUS, HEIGHT//2 + PADDLE_RADIUS,
        fill="blue", outline="white"
    )
    
    paddle_b = canvas.create_oval(
        3*WIDTH//4 - PADDLE_RADIUS, HEIGHT//2 - PADDLE_RADIUS,
        3*WIDTH//4 + PADDLE_RADIUS, HEIGHT//2 + PADDLE_RADIUS,
        fill="red", outline="white"
    )
    
    # Шайба
    ball = canvas.create_oval(
        WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS,
        WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS,
        fill="white", outline="black"
    )
    
    # Разметка поля
    canvas.create_line(WIDTH//2, 0, WIDTH//2, HEIGHT, fill="gray", dash=(5, 5))
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, outline="white", width=3)
    
    # Ворота
    goal_width = 200
    canvas.create_rectangle(0, HEIGHT//2-goal_width//2, 10, HEIGHT//2+goal_width//2, 
                          fill="gray", outline="white")
    canvas.create_rectangle(WIDTH-10, HEIGHT//2-goal_width//2, WIDTH, HEIGHT//2+goal_width//2, 
                          fill="gray", outline="white")

def restart_game():
    global score_a, score_b, ball_is_moving, is_paused, game_over
    
    hide_pause_menu()
    if 'end_menu' in globals():
        end_menu.destroy()
    
    # Сброс состояния
    is_paused = False
    game_over = False
    score_a = 0
    score_b = 0
    ball_is_moving = False
    
    # Очистка поля (кроме фона)
    items = canvas.find_all()
    for item in items:
        if "background" not in canvas.gettags(item):
            canvas.delete(item)
    
    # Новая игра
    init_game()
    reset_ball()

def key_pressed(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = True
    if event.keycode == 32:  # Пробел
        toggle_pause()

def key_released(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = False

def toggle_pause():
    global is_paused
    if not game_over:
        is_paused = not is_paused
        if is_paused:
            show_pause_menu()
        else:
            hide_pause_menu()

def show_pause_menu():
    if 'pause_menu' in globals():
        pause_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

def hide_pause_menu():
    if 'pause_menu' in globals():
        pause_menu.place_forget()

def move_paddles():
    if not is_paused and not game_over:
        # Игрок A (WASD)
        x1, y1, x2, y2 = canvas.coords(paddle_a)
        if keys_pressed[87] and y1 > 0:  # W
            canvas.move(paddle_a, 0, -PADDLE_SPEED)
        if keys_pressed[83] and y2 < HEIGHT:  # S
            canvas.move(paddle_a, 0, PADDLE_SPEED)
        if keys_pressed[65] and x1 > 0:  # A
            canvas.move(paddle_a, -PADDLE_SPEED, 0)
        if keys_pressed[68] and x2 < WIDTH//2:  # D
            canvas.move(paddle_a, PADDLE_SPEED, 0)

        # Игрок B (Стрелки)
        x1, y1, x2, y2 = canvas.coords(paddle_b)
        if keys_pressed[38] and y1 > 0:  # Вверх
            canvas.move(paddle_b, 0, -PADDLE_SPEED)
        if keys_pressed[40] and y2 < HEIGHT:  # Вниз
            canvas.move(paddle_b, 0, PADDLE_SPEED)
        if keys_pressed[37] and x1 > WIDTH//2:  # Влево
            canvas.move(paddle_b, -PADDLE_SPEED, 0)
        if keys_pressed[39] and x2 < WIDTH:  # Вправо
            canvas.move(paddle_b, PADDLE_SPEED, 0)

        check_ball_collision()

    root.after(20, move_paddles)

def check_ball_collision():
    global ball_speed_x, ball_speed_y, ball_is_moving

    ball_coords = canvas.coords(ball)
    paddle_a_coords = canvas.coords(paddle_a)
    paddle_b_coords = canvas.coords(paddle_b)

    # Столкновение с битой A
    if (ball_coords[0] <= paddle_a_coords[2] and ball_coords[2] >= paddle_a_coords[0] and
        ball_coords[1] <= paddle_a_coords[3] and ball_coords[3] >= paddle_a_coords[1]):
        
        if not ball_is_moving:
            start_ball_movement()
        else:
            handle_collision(paddle_a_coords, ball_coords)

    # Столкновение с битой B
    if (ball_coords[0] <= paddle_b_coords[2] and ball_coords[2] >= paddle_b_coords[0] and
        ball_coords[1] <= paddle_b_coords[3] and ball_coords[3] >= paddle_b_coords[1]):
        
        if not ball_is_moving:
            start_ball_movement()
        else:
            handle_collision(paddle_b_coords, ball_coords)

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

    ball_speed_x = BALL_SPEED * dx
    ball_speed_y = BALL_SPEED * dy

    overlap = PADDLE_RADIUS + BALL_RADIUS - length + 5
    canvas.move(ball, dx * overlap, dy * overlap)

def start_ball_movement():
    global ball_speed_x, ball_speed_y, ball_is_moving
    if not ball_is_moving:
        ball_speed_x = BALL_SPEED  # Начинаем движение вправо
        ball_speed_y = 0           # Без вертикального смещения
        ball_is_moving = True

def update_ball():
    global ball_speed_x, ball_speed_y, score_a, score_b, game_over
    
    if is_paused or game_over:
        root.after(20, update_ball)
        return
    
    if ball_is_moving:
        x1, y1, x2, y2 = canvas.coords(ball)
        
        # Отскок от стен
        if y1 <= 0 or y2 >= HEIGHT:
            ball_speed_y *= -1
        if x1 <= 0 or x2 >= WIDTH:
            ball_speed_x *= -1
            
        # Проверка голов
        goal_width = 200
        goal_top = HEIGHT//2 - goal_width//2
        goal_bottom = HEIGHT//2 + goal_width//2
        
        if x1 <= 10 and goal_top <= y1 <= goal_bottom and goal_top <= y2 <= goal_bottom:
            score_b += 1
            reset_ball()
        elif x2 >= WIDTH-10 and goal_top <= y1 <= goal_bottom and goal_top <= y2 <= goal_bottom:
            score_a += 1
            reset_ball()
        else:
            canvas.move(ball, ball_speed_x, ball_speed_y)

        # Обновление счета
        canvas.itemconfig(score_text, text=f"Синий: {score_a}  Красный: {score_b}")

        if score_a >= WIN_SCORE or score_b >= WIN_SCORE:
            end_game()
    
    root.after(20, update_ball)

def reset_ball():
    global ball_speed_x, ball_speed_y, ball_is_moving
    canvas.coords(ball, 
                 WIDTH//2 - BALL_RADIUS, 
                 HEIGHT//2 - BALL_RADIUS, 
                 WIDTH//2 + BALL_RADIUS, 
                 HEIGHT//2 + BALL_RADIUS)
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False

def end_game():
    global game_over, end_menu
    
    game_over = True
    winner = "Синий игрок" if score_a >= WIN_SCORE else "Красный игрок"
    
    end_menu = Frame(root, bg="black", padx=40, pady=30)
    Label(end_menu, text=f"{winner} победил!", font=("Arial", 36, 'bold'), 
          bg="black", fg="white").pack(pady=15)
    
    Button(end_menu, text="Заново", font=("Arial", 24), 
           command=lambda: [end_menu.destroy(), restart_game()], 
           bg="#333", fg="white", width=15).pack(pady=10)
    Button(end_menu, text="В главное меню", font=("Arial", 24), 
           command=return_to_game_menu, bg="#333", fg="white", width=15).pack(pady=10)
    
    end_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

# Кнопки интерфейса
mode_buttons = []

btn = Button(root, text='Начать играть', width=35, height=2, bg='#080675', 
            fg='#AFD7FF', font=('impact', 20, 'bold'), command=change_image)
btn.place(relx=0.5, rely=0.5, anchor='center')

exit_btn_main = Button(root, text='Выход', width=35, height=2, bg='#080675', 
                      fg='#AFD7FF', font=('impact', 20, 'bold'), command=exit_game)
exit_btn_main.place(relx=0.5, rely=0.65, anchor='center')

main_menu_btn = Button(root, text='Главное меню', width=35, height=2, bg='#080675', 
                      fg='#AFD7FF', font=('impact', 20, 'bold'), command=return_to_main_menu)
main_menu_btn.place_forget()

# Запуск приложения
root.mainloop()