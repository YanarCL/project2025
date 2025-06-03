from tkinter import *
import random

# Настройки игры
WIDTH = 1000  # Ширина окна
HEIGHT = 600  # Высота окна
PADDLE_RADIUS = 30  # Радиус биты
BALL_RADIUS = 15  # Радиус шайбы
PADDLE_SPEED = 5  # Скорость движения бит
BALL_SPEED_X = 4  # Горизонтальная скорость шайбы
BALL_SPEED_Y = 4  # Вертикальная скорость шайбы
WIN_SCORE = 10  # Очки для победы

# Инициализация окна
root = Tk()
root.title("Аэрохоккей")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Счёт
score_a = 0
score_b = 0
score_label = Label(root, text=f"Игрок A: {score_a}  Игрок B: {score_b}", font=("Arial", 20), fg="white", bg="black")
score_label.pack()

# Элементы игры
# Бита игрока A (управление WASD/ЦФЫВ)
paddle_a = canvas.create_oval(
    WIDTH // 4 - PADDLE_RADIUS, HEIGHT // 2 - PADDLE_RADIUS,
    WIDTH // 4 + PADDLE_RADIUS, HEIGHT // 2 + PADDLE_RADIUS,
    fill="blue"
)

# Бита игрока B (управление стрелками)
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
goal_width = 200  # Ширина ворот
canvas.create_rectangle(0, HEIGHT // 2 - goal_width // 2, 10, HEIGHT // 2 + goal_width // 2, fill="gray")  # Ворота игрока A
canvas.create_rectangle(WIDTH - 10, HEIGHT // 2 - goal_width // 2, WIDTH, HEIGHT // 2 + goal_width // 2, fill="gray")  # Ворота игрока B

# Линия-ограничитель по середине
canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill="white", dash=(5, 5))

# Начальная скорость шайбы
ball_speed_x = 0  # Шайба не двигается до первого касания
ball_speed_y = 0
ball_is_moving = False  # Флаг, указывающий, движется ли шайба

# Состояние клавиш
keys_pressed = {
    'w': False, 'ц': False,  # Вверх
    'a': False, 'ф': False,  # Влево
    's': False, 'ы': False,  # Вниз
    'd': False, 'в': False,  # Вправо
    'Up': False, 'Down': False, 'Left': False, 'Right': False  # Управление для игрока B
}

# Функции для отслеживания нажатия и отпускания клавиш
def key_pressed(event):
    if event.keysym in keys_pressed:
        keys_pressed[event.keysym] = True

def key_released(event):
    if event.keysym in keys_pressed:
        keys_pressed[event.keysym] = False

# Привязка событий клавиш
root.bind("<KeyPress>", key_pressed)
root.bind("<KeyRelease>", key_released)

# Движение бит
def move_paddles():
    # Движение биты игрока A (WASD/ЦФЫВ)
    x1, y1, x2, y2 = canvas.coords(paddle_a)
    if (keys_pressed['w'] or keys_pressed['ц']) and y1 > 0:  # Вверх
        canvas.move(paddle_a, 0, -PADDLE_SPEED)
    if (keys_pressed['s'] or keys_pressed['ы']) and y2 < HEIGHT:  # Вниз
        canvas.move(paddle_a, 0, PADDLE_SPEED)
    if (keys_pressed['a'] or keys_pressed['ф']) and x1 > 0:  # Влево
        canvas.move(paddle_a, -PADDLE_SPEED, 0)
    if (keys_pressed['d'] or keys_pressed['в']) and x2 < WIDTH // 2:  # Вправо (ограничение на половину поля)
        canvas.move(paddle_a, PADDLE_SPEED, 0)

    # Движение биты игрока B (стрелки)
    x1, y1, x2, y2 = canvas.coords(paddle_b)
    if keys_pressed['Up'] and y1 > 0:  # Вверх
        canvas.move(paddle_b, 0, -PADDLE_SPEED)
    if keys_pressed['Down'] and y2 < HEIGHT:  # Вниз
        canvas.move(paddle_b, 0, PADDLE_SPEED)
    if keys_pressed['Left'] and x1 > WIDTH // 2:  # Влево (ограничение на половину поля)
        canvas.move(paddle_b, -PADDLE_SPEED, 0)
    if keys_pressed['Right'] and x2 < WIDTH:  # Вправо
        canvas.move(paddle_b, PADDLE_SPEED, 0)

    # Проверка касания шайбы битами
    check_ball_collision()

    # Планируем следующее обновление
    root.after(20, move_paddles)

# Проверка касания шайбы битами
def check_ball_collision():
    global ball_speed_x, ball_speed_y, ball_is_moving

    x1, y1, x2, y2 = canvas.coords(ball)
    paddle_a_coords = canvas.coords(paddle_a)
    paddle_b_coords = canvas.coords(paddle_b)

    # Проверка столкновения с битой A
    if (x1 <= paddle_a_coords[2] and x2 >= paddle_a_coords[0] and
        y1 <= paddle_a_coords[3] and y2 >= paddle_a_coords[1]):
        if not ball_is_moving:
            start_ball_movement()
        else:
            # Вычисляем центр биты и шайбы
            paddle_center_x = (paddle_a_coords[0] + paddle_a_coords[2]) / 2
            paddle_center_y = (paddle_a_coords[1] + paddle_a_coords[3]) / 2
            ball_center_x = (x1 + x2) / 2
            ball_center_y = (y1 + y2) / 2

            # Вектор от центра биты к центру шайбы
            dx = ball_center_x - paddle_center_x
            dy = ball_center_y - paddle_center_y

            # Нормализуем вектор
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length != 0:
                dx /= length
                dy /= length

            # Меняем направление шайбы
            ball_speed_x = dx * BALL_SPEED_X
            ball_speed_y = dy * BALL_SPEED_Y

    # Проверка столкновения с битой B
    if (x1 <= paddle_b_coords[2] and x2 >= paddle_b_coords[0] and
        y1 <= paddle_b_coords[3] and y2 >= paddle_b_coords[1]):
        if not ball_is_moving:
            start_ball_movement()
        else:
            # Вычисляем центр биты и шайбы
            paddle_center_x = (paddle_b_coords[0] + paddle_b_coords[2]) / 2
            paddle_center_y = (paddle_b_coords[1] + paddle_b_coords[3]) / 2
            ball_center_x = (x1 + x2) / 2
            ball_center_y = (y1 + y2) / 2

            # Вектор от центра биты к центру шайбы
            dx = ball_center_x - paddle_center_x
            dy = ball_center_y - paddle_center_y

            # Нормализуем вектор
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length != 0:
                dx /= length
                dy /= length

            # Меняем направление шайбы
            ball_speed_x = dx * BALL_SPEED_X
            ball_speed_y = dy * BALL_SPEED_Y

# Логика игры
def update_ball():
    global ball_speed_x, ball_speed_y, score_a, score_b, ball_is_moving

    if ball_is_moving:
        # Движение шайбы
        canvas.move(ball, ball_speed_x, ball_speed_y)
        x1, y1, x2, y2 = canvas.coords(ball)

        # Отскок от стен
        if x1 <= 0 or x2 >= WIDTH:
            ball_speed_x = -ball_speed_x
        if y1 <= 0 or y2 >= HEIGHT:
            ball_speed_y = -ball_speed_y

        # Голы
        if x1 <= 10 and HEIGHT // 2 - goal_width // 2 <= y1 <= HEIGHT // 2 + goal_width // 2:
            score_b += 1
            reset_ball()
        if x2 >= WIDTH - 10 and HEIGHT // 2 - goal_width // 2 <= y1 <= HEIGHT // 2 + goal_width // 2:
            score_a += 1
            reset_ball()

    # Обновление счёта
    score_label.config(text=f"Игрок A: {score_a}  Игрок B: {score_b}")

    # Проверка на победу
    if score_a >= WIN_SCORE or score_b >= WIN_SCORE:
        end_game()
    else:
        root.after(20, update_ball)

# Сброс шайбы в центр
def reset_ball():
    global ball_speed_x, ball_speed_y, ball_is_moving
    canvas.coords(ball, WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS)
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False  # Шайба не двигается до касания битой

# Запуск движения шайбы после касания битой
def start_ball_movement():
    global ball_speed_x, ball_speed_y, ball_is_moving
    if not ball_is_moving:
        ball_speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
        ball_speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
        ball_is_moving = True

# Завершение игры
def end_game():
    winner = "Игрок A" if score_a >= WIN_SCORE else "Игрок B"
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"{winner} победил!", font=("Arial", 40), fill="white")
    restart_button.pack()

# Перезапуск игры
def restart_game():
    global score_a, score_b
    score_a = 0
    score_b = 0
    score_label.config(text=f"Игрок A: {score_a}  Игрок B: {score_b}")
    canvas.delete("all")
    reset_ball()
    restart_button.pack_forget()
    update_ball()

# Кнопка перезапуска
restart_button = Button(root, text="Перезапуск", font=("Arial", 20), command=restart_game)
restart_button.pack_forget()

# Запуск игры
reset_ball()
update_ball()
move_paddles()  # Запуск движения бит

root.mainloop()