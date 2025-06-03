from tkinter import *
import math
import random
from PIL import Image, ImageTk

# Настройки игры
WIDTH = 1000
HEIGHT = 500
PADDLE_RADIUS = 30
BALL_RADIUS = 15
PADDLE_SPEED = 8
BALL_SPEED = 14
WIN_SCORE = 4

# Инициализация окна
root = Tk()
root.title("Аэрохоккей")
root.attributes('-fullscreen', True)

# Загрузка фонового изображения
def load_background(image_path, width=None, height=None):
    try:
        image = Image.open(image_path)
        if width and height:
            image = image.resize((width, height))
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

# Загрузка фоновых изображений
background_image = load_background("D:\Stadion.jpg")
if background_image:
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

canvas_background_image = load_background("D:/2 курс/Практика 2 курс 2 семестр/6662559.jpg", WIDTH, HEIGHT)
if canvas_background_image:
    canvas.create_image(0, 0, anchor=NW, image=canvas_background_image)

# Счёт
score_a = 0
score_b = 0
score_text = canvas.create_text(WIDTH // 2, 30, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}", 
                              font=("Arial", 30), fill="black")

# Инициализация игровых элементов
def init_game():
    global paddle_a, paddle_b, ball
    
    # Бита игрока A
    paddle_a = canvas.create_oval(
        WIDTH // 4 - PADDLE_RADIUS, HEIGHT // 2 - PADDLE_RADIUS,
        WIDTH // 4 + PADDLE_RADIUS, HEIGHT // 2 + PADDLE_RADIUS,
        fill="blue"
    )

    # Бита игрока B
    paddle_b = canvas.create_oval(
        3 * WIDTH // 4 - PADDLE_RADIUS, HEIGHT // 2 - PADDLE_RADIUS,
        3 * WIDTH // 4 + PADDLE_RADIUS, HEIGHT // 2 + PADDLE_RADIUS,
        fill="red"
    )

    # Шайба
    ball = canvas.create_oval(
        WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS,
        WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS,
        fill="white"
    )

    # Ворота
    goal_width = 200
    canvas.create_rectangle(0, HEIGHT // 2 - goal_width // 2, 10, HEIGHT // 2 + goal_width // 2, fill="gray")
    canvas.create_rectangle(WIDTH - 10, HEIGHT // 2 - goal_width // 2, WIDTH, HEIGHT // 2 + goal_width // 2, fill="gray")

    # Разметка поля
    canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill="gray", dash=(5, 5))
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, outline="white", width=2)

# Начальная скорость шайбы
ball_speed_x = 0
ball_speed_y = 0
ball_is_moving = False

# Состояние клавиш
keys_pressed = {
    87: False,   # W
    65: False,   # A
    83: False,   # S
    68: False,   # D
    38: False,   # Стрелка вверх
    40: False,   # Стрелка вниз
    37: False,   # Стрелка влево
    39: False,   # Стрелка вправо
    32: False    # Пробел
}

# Перезапуск игры
def restart_game():
    global score_a, score_b, ball_speed_x, ball_speed_y, ball_is_moving, is_paused, game_over
    
    score_a = 0
    score_b = 0
    is_paused = False
    game_over = False
    
    canvas.delete("all")
    if canvas_background_image:
        canvas.create_image(0, 0, anchor=NW, image=canvas_background_image)
    
    init_game()
    
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False
    
    canvas.itemconfig(score_text, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}")
    update_ball()

# Обработчики клавиш
def key_pressed(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = True
    if event.keycode == 32:  # Пробел
        toggle_pause()

def key_released(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = False

root.bind("<KeyPress>", key_pressed)
root.bind("<KeyRelease>", key_released)

# Пауза
is_paused = False
game_over = False

def toggle_pause():
    global is_paused
    if not game_over:  # Не позволяем паузировать после окончания игры
        is_paused = not is_paused
        if is_paused:
            show_pause_menu()
        else:
            hide_pause_menu()

def show_pause_menu():
    pause_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

def hide_pause_menu():
    pause_menu.place_forget()

# Меню паузы
pause_menu = Frame(root, bg="black", padx=20, pady=20)
Label(pause_menu, text="ПАУЗА", font=("Arial", 30), bg="black", fg="white").pack(pady=10)

continue_button = Button(pause_menu, text="Продолжить", font=("Arial", 20), command=toggle_pause)
restart_button_pause = Button(pause_menu, text="Заново", font=("Arial", 20), command=restart_game)
exit_button = Button(pause_menu, text="Выход", font=("Arial", 20), command=root.quit)

continue_button.pack(pady=10, fill=X)
restart_button_pause.pack(pady=10, fill=X)
exit_button.pack(pady=10, fill=X)

pause_menu.place_forget()

# Движение бит
def move_paddles():
    if not is_paused and not game_over:
        # Движение биты игрока A
        x1, y1, x2, y2 = canvas.coords(paddle_a)
        if keys_pressed[87] and y1 > 0:  # Вверх (W)
            canvas.move(paddle_a, 0, -PADDLE_SPEED)
        if keys_pressed[83] and y2 < HEIGHT:  # Вниз (S)
            canvas.move(paddle_a, 0, PADDLE_SPEED)
        if keys_pressed[65] and x1 > 0:  # Влево (A)
            canvas.move(paddle_a, -PADDLE_SPEED, 0)
        if keys_pressed[68] and x2 < WIDTH // 2:  # Вправо (D)
            canvas.move(paddle_a, PADDLE_SPEED, 0)

        # Движение биты игрока B
        x1, y1, x2, y2 = canvas.coords(paddle_b)
        if keys_pressed[38] and y1 > 0:  # Вверх
            canvas.move(paddle_b, 0, -PADDLE_SPEED)
        if keys_pressed[40] and y2 < HEIGHT:  # Вниз
            canvas.move(paddle_b, 0, PADDLE_SPEED)
        if keys_pressed[37] and x1 > WIDTH // 2:  # Влево
            canvas.move(paddle_b, -PADDLE_SPEED, 0)
        if keys_pressed[39] and x2 < WIDTH:  # Вправо
            canvas.move(paddle_b, PADDLE_SPEED, 0)

        check_ball_collision()

    root.after(20, move_paddles)

# Проверка столкновений с защитой от залипания
def check_ball_collision():
    global ball_speed_x, ball_speed_y, ball_is_moving

    ball_coords = canvas.coords(ball)
    paddle_a_coords = canvas.coords(paddle_a)
    paddle_b_coords = canvas.coords(paddle_b)

    # Проверка столкновения с битой A
    if (ball_coords[0] <= paddle_a_coords[2] and ball_coords[2] >= paddle_a_coords[0] and
        ball_coords[1] <= paddle_a_coords[3] and ball_coords[3] >= paddle_a_coords[1]):
        
        if not ball_is_moving:
            start_ball_movement()
        else:
            paddle_center_x = (paddle_a_coords[0] + paddle_a_coords[2]) / 2
            paddle_center_y = (paddle_a_coords[1] + paddle_a_coords[3]) / 2
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

    # Проверка столкновения с битой B
    if (ball_coords[0] <= paddle_b_coords[2] and ball_coords[2] >= paddle_b_coords[0] and
        ball_coords[1] <= paddle_b_coords[3] and ball_coords[3] >= paddle_b_coords[1]):
        
        if not ball_is_moving:
            start_ball_movement()
        else:
            paddle_center_x = (paddle_b_coords[0] + paddle_b_coords[2]) / 2
            paddle_center_y = (paddle_b_coords[1] + paddle_b_coords[3]) / 2
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

# Запуск движения шайбы
def start_ball_movement():
    global ball_speed_x, ball_speed_y, ball_is_moving
    if not ball_is_moving:
        ball_speed_x = BALL_SPEED if random.random() > 0.5 else -BALL_SPEED
        ball_speed_y = BALL_SPEED if random.random() > 0.5 else -BALL_SPEED
        ball_is_moving = True

# Логика игры
def update_ball():
    global ball_speed_x, ball_speed_y, score_a, score_b, ball_is_moving, game_over

    if is_paused or game_over:
        root.after(20, update_ball)
        return

    if ball_is_moving:
        canvas.move(ball, ball_speed_x, ball_speed_y)
        x1, y1, x2, y2 = canvas.coords(ball)

        # Отскок от стен
        if x1 <= 0:
            x1 = BALL_RADIUS
            ball_speed_x = abs(ball_speed_x)
        if x2 >= WIDTH:
            x2 = WIDTH - BALL_RADIUS
            ball_speed_x = -abs(ball_speed_x)
        if y1 <= 0:
            y1 = BALL_RADIUS
            ball_speed_y = abs(ball_speed_y)
        if y2 >= HEIGHT:
            y2 = HEIGHT - BALL_RADIUS
            ball_speed_y = -abs(ball_speed_y)

        canvas.coords(ball, x1, y1, x1 + 2 * BALL_RADIUS, y1 + 2 * BALL_RADIUS)

        # Голы
        goal_width = 200
        if x1 <= 10 and HEIGHT // 2 - goal_width // 2 <= y1 <= HEIGHT // 2 + goal_width // 2:
            score_b += 1
            reset_ball()
        if x2 >= WIDTH - 10 and HEIGHT // 2 - goal_width // 2 <= y1 <= HEIGHT // 2 + goal_width // 2:
            score_a += 1
            reset_ball()

    canvas.itemconfig(score_text, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}")

    if score_a >= WIN_SCORE or score_b >= WIN_SCORE:
        end_game()
    else:
        root.after(20, update_ball)

# Сброс шайбы
def reset_ball():
    global ball_speed_x, ball_speed_y, ball_is_moving
    canvas.coords(ball, WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, 
                 WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS)
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False

# Завершение игры
def end_game():
    global game_over
    game_over = True
    winner = "Игрок Синий" if score_a >= WIN_SCORE else "Игрок Красный"
    
    # Создаем меню окончания игры
    end_menu = Frame(root, bg="black", padx=20, pady=20)
    Label(end_menu, text=f"{winner} победил!", font=("Arial", 30), bg="black", fg="white").pack(pady=10)
    
    restart_button_end = Button(end_menu, text="Заново", font=("Arial", 20), command=lambda: [end_menu.destroy(), restart_game()])
    exit_button_end = Button(end_menu, text="Выход", font=("Arial", 20), command=root.quit)
    
    restart_button_end.pack(pady=10, fill=X)
    exit_button_end.pack(pady=10, fill=X)
    
    end_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

# Инициализация и запуск игры
init_game()
reset_ball()
update_ball()
move_paddles()

root.mainloop()