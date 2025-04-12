from tkinter import *
import random
import math
from PIL import Image, ImageTk

# Настройки игры
WIDTH = 1000  # Ширина игрового поля
HEIGHT = 500  # Высота игрового поля
PADDLE_RADIUS = 30  # Радиус биты
BALL_RADIUS = 15  # Радиус шайбы
PADDLE_SPEED = 8  # Скорость движения бит
BALL_SPEED = 14  # Скорость шайбы
WIN_SCORE = 4  # Очки для победы

# Инициализация окна
root = Tk()
root.title("Аэрохоккей")
root.attributes('-fullscreen', True)  # Открыть окно в полный экран

# Загрузка фонового изображения
def load_background(image_path, width=None, height=None):
    try:
        image = Image.open(image_path)
        if width and height:
            image = image.resize((width, height))  # Изменяем размер, если указаны параметры
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Ошибка при загрузке фонового изображения: {e}")
        return None

# Загрузка фонового изображения для основного окна
background_image = load_background("D:\Stadion.jpg")
if background_image:
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Растягиваем на весь экран

# Создание Canvas для игрового поля
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Размещаем Canvas по центру экрана

# Загрузка фонового изображения для Canvas (игрового поля)
canvas_background_image = load_background("D:/2 курс/Практика 2 курс 2 семестр/6662559.jpg", WIDTH, HEIGHT)
if canvas_background_image:
    canvas.create_image(0, 0, anchor=NW, image=canvas_background_image)

# Счёт
score_a = 0
score_b = 0
score_text = canvas.create_text(WIDTH // 2, 30, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}", font=("Arial", 30), fill="black")

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
canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill="gray", dash=(5, 5))

# Визуальные границы игрового поля (ярко-зеленые)
canvas.create_rectangle(0, 0, WIDTH, HEIGHT, outline="white", width=2)

# Начальная скорость шайбы
ball_speed_x = 0  # Шайба не двигается до первого касания
ball_speed_y = 0
ball_is_moving = False  # Флаг, указывающий, движется ли шайба

# Состояние клавиш
keys_pressed = {
    87: False,  # W (Вверх)
    65: False,  # A (Влево)
    83: False,  # S (Вниз)
    68: False,  # D (Вправо)
    38: False,  # Стрелка вверх (Вверх для игрока B)
    40: False,  # Стрелка вниз (Вниз для игрока B)
    37: False,  # Стрелка влево (Влево для игрока B)
    39: False,  # Стрелка вправо (Вправо для игрока B)
    32: False   # Пробел (Пауза)
}

# Функции для отслеживания нажатия и отпускания клавиш
def key_pressed(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = True
    if event.keycode == 32:  # Пробел
        toggle_pause()

def key_released(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = False

# Привязка событий клавиш
root.bind("<KeyPress>", key_pressed)
root.bind("<KeyRelease>", key_released)

# Пауза
is_paused = False

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        show_pause_menu()
    else:
        hide_pause_menu()

def show_pause_menu():
    pause_menu.pack()

def hide_pause_menu():
    pause_menu.pack_forget()

# Меню паузы
pause_menu = Frame(root, bg="black")
continue_button = Button(pause_menu, text="Продолжить", font=("Arial", 20), command=toggle_pause)
exit_button = Button(pause_menu, text="Выйти", font=("Arial", 20), command=root.quit)
continue_button.pack(pady=10)
exit_button.pack(pady=10)
pause_menu.pack_forget()

# Движение бит
def move_paddles():
    # Движение биты игрока A (WASD)
    x1, y1, x2, y2 = canvas.coords(paddle_a)
    if keys_pressed[87] and y1 > 0:  # Вверх (W)
        canvas.move(paddle_a, 0, -PADDLE_SPEED)
    if keys_pressed[83] and y2 < HEIGHT:  # Вниз (S)
        canvas.move(paddle_a, 0, PADDLE_SPEED)
    if keys_pressed[65] and x1 > 0:  # Влево (A)
        canvas.move(paddle_a, -PADDLE_SPEED, 0)
    if keys_pressed[68] and x2 < WIDTH // 2:  # Вправо (D)
        canvas.move(paddle_a, PADDLE_SPEED, 0)

    # Движение биты игрока B (стрелки)
    x1, y1, x2, y2 = canvas.coords(paddle_b)
    if keys_pressed[38] and y1 > 0:  # Вверх (Стрелка вверх)
        canvas.move(paddle_b, 0, -PADDLE_SPEED)
    if keys_pressed[40] and y2 < HEIGHT:  # Вниз (Стрелка вниз)
        canvas.move(paddle_b, 0, PADDLE_SPEED)
    if keys_pressed[37] and x1 > WIDTH // 2:  # Влево (Стрелка влево)
        canvas.move(paddle_b, -PADDLE_SPEED, 0)
    if keys_pressed[39] and x2 < WIDTH:  # Вправо (Стрелка вправо)
        canvas.move(paddle_b, PADDLE_SPEED, 0)

    # Проверка касания шайбы битами
    if not is_paused:
        check_ball_collision()

    # Планируем следующее обновление
    root.after(20, move_paddles)

# Улучшенная проверка столкновений
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

            # Добавляем случайное отклонение для реализма
            angle = math.atan2(dy, dx) + random.uniform(-0.2, 0.2)
            ball_speed_x = BALL_SPEED * math.cos(angle)
            ball_speed_y = BALL_SPEED * math.sin(angle)

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

            # Добавляем случайное отклонение для реализма
            angle = math.atan2(dy, dx) + random.uniform(-0.2, 0.2)
            ball_speed_x = BALL_SPEED * math.cos(angle)
            ball_speed_y = BALL_SPEED * math.sin(angle)

# Логика игры
def update_ball():
    global ball_speed_x, ball_speed_y, score_a, score_b, ball_is_moving

    if is_paused:
        root.after(20, update_ball)
        return

    if ball_is_moving:
        # Движение шайбы
        canvas.move(ball, ball_speed_x, ball_speed_y)
        x1, y1, x2, y2 = canvas.coords(ball)

        # Отскок от стен с корректировкой координат
        if x1 <= 0:
            x1 = BALL_RADIUS
            ball_speed_x = abs(ball_speed_x)  # Убедимся, что шайба движется вправо
        if x2 >= WIDTH:
            x2 = WIDTH - BALL_RADIUS
            ball_speed_x = -abs(ball_speed_x)  # Убедимся, что шайба движется влево
        if y1 <= 0:
            y1 = BALL_RADIUS
            ball_speed_y = abs(ball_speed_y)  # Убедимся, что шайба движется вниз
        if y2 >= HEIGHT:
            y2 = HEIGHT - BALL_RADIUS
            ball_speed_y = -abs(ball_speed_y)  # Убедимся, что шайба движется вверх

        # Обновляем координаты шайбы, сохраняя её круглую форму
        canvas.coords(ball, x1, y1, x1 + 2 * BALL_RADIUS, y1 + 2 * BALL_RADIUS)

        # Голы
        if x1 <= 10 and HEIGHT // 2 - goal_width // 2 <= y1 <= HEIGHT // 2 + goal_width // 2:
            score_b += 1
            reset_ball()
        if x2 >= WIDTH - 10 and HEIGHT // 2 - goal_width // 2 <= y1 <= HEIGHT // 2 + goal_width // 2:
            score_a += 1
            reset_ball()

    # Обновление счёта
    canvas.itemconfig(score_text, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}")

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
        ball_speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
        ball_speed_y = random.choice([-BALL_SPEED, BALL_SPEED])
        ball_is_moving = True

# Завершение игры
def end_game():
    winner = "Игрок Синий" if score_a >= WIN_SCORE else "Игрок Красный"
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"{winner} победил!", font=("Arial", 40), fill="black")
    restart_button.pack()

# Перезапуск игры
def restart_game():
    global score_a, score_b
    score_a = 0
    score_b = 0
    canvas.itemconfig(score_text, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}")
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