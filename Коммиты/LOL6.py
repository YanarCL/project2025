from tkinter import *
import math
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
background_image = load_background("D:\FonForPlay.png")
if background_image:
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

canvas_background_image = load_background("D:\GameFone.png", WIDTH, HEIGHT)
if canvas_background_image:
    canvas.create_image(0, 0, anchor=NW, image=canvas_background_image)

# Глобальные переменные
score_a = 0
score_b = 0
score_text = None
paddle_a = None
paddle_b = None
ball = None
ball_speed_x = 0
ball_speed_y = 0
ball_is_moving = False
is_paused = False
game_over = False

# Состояние клавиш
keys_pressed = {
    87: False,  # W
    65: False,  # A
    83: False,  # S
    68: False,  # D
    38: False,  # Стрелка вверх
    40: False,  # Стрелка вниз
    37: False,  # Стрелка влево
    39: False,  # Стрелка вправо
    32: False   # Пробел
}

# Инициализация игровых элементов
def init_game():
    global paddle_a, paddle_b, ball, score_text
    
    # Создаем текст счета только при первом запуске
    if score_text is None:
        score_text = canvas.create_text(WIDTH // 2, 30, 
                                      text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}", 
                                      font=("Arial", 30), fill="black")
    else:
        # Обновляем текст счета
        canvas.itemconfig(score_text, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}")

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

    ball = canvas.create_oval(
        WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS,
        WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS,
        fill="white", outline="black"
    )

    # Рисуем ворота
    goal_width = 200
    canvas.create_rectangle(0, HEIGHT // 2 - goal_width // 2, 10, HEIGHT // 2 + goal_width // 2, 
                          fill="gray", outline="black")
    canvas.create_rectangle(WIDTH - 10, HEIGHT // 2 - goal_width // 2, WIDTH, HEIGHT // 2 + goal_width // 2, 
                          fill="gray", outline="black")

    # Рисуем разметку поля
    canvas.create_line(WIDTH // 2, 0, WIDTH // 2, HEIGHT, fill="gray", dash=(5, 5))
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, outline="white", width=3)

# Перезапуск игры
def restart_game():
    global ball_speed_x, ball_speed_y, ball_is_moving, is_paused, game_over, score_a, score_b
    
    # Закрываем меню паузы и окончания игры
    hide_pause_menu()
    if 'end_menu' in globals():
        end_menu.destroy()
    
    # Сброс состояния игры
    is_paused = False
    game_over = False
    score_a = 0
    score_b = 0
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False
    
    # Удаляем все элементы, кроме счета
    items = canvas.find_all()
    for item in items:
        if item != score_text:
            canvas.delete(item)
    
    # Восстанавливаем фон
    if canvas_background_image:
        canvas.create_image(0, 0, anchor=NW, image=canvas_background_image)
        canvas.tag_raise(score_text)  # Поднимаем счет над фоном
    
    # Переинициализация игры
    init_game()
    reset_ball()

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

# Меню паузы
pause_menu = Frame(root, bg="black", padx=40, pady=30)
Label(pause_menu, text="ПАУЗА", font=("Arial", 36, 'bold'), bg="black", fg="white").pack(pady=15)

Button(pause_menu, text="Продолжить", font=("Arial", 24), 
      command=toggle_pause, bg="#333", fg="white", width=15).pack(pady=10)
Button(pause_menu, text="Заново", font=("Arial", 24), 
      command=restart_game, bg="#333", fg="white", width=15).pack(pady=10)
Button(pause_menu, text="Выход", font=("Arial", 24), 
      command=root.quit, bg="#333", fg="white", width=15).pack(pady=10)

pause_menu.place_forget()

# Движение бит
def move_paddles():
    if not is_paused and not game_over:
        # Движение биты игрока A (WASD)
        x1, y1, x2, y2 = canvas.coords(paddle_a)
        if keys_pressed[87] and y1 > 0:  # W
            canvas.move(paddle_a, 0, -PADDLE_SPEED)
        if keys_pressed[83] and y2 < HEIGHT:  # S
            canvas.move(paddle_a, 0, PADDLE_SPEED)
        if keys_pressed[65] and x1 > 0:  # A
            canvas.move(paddle_a, -PADDLE_SPEED, 0)
        if keys_pressed[68] and x2 < WIDTH // 2:  # D
            canvas.move(paddle_a, PADDLE_SPEED, 0)

        # Движение биты игрока B (Стрелки)
        x1, y1, x2, y2 = canvas.coords(paddle_b)
        if keys_pressed[38] and y1 > 0:  # Стрелка вверх
            canvas.move(paddle_b, 0, -PADDLE_SPEED)
        if keys_pressed[40] and y2 < HEIGHT:  # Стрелка вниз
            canvas.move(paddle_b, 0, PADDLE_SPEED)
        if keys_pressed[37] and x1 > WIDTH // 2:  # Стрелка влево
            canvas.move(paddle_b, -PADDLE_SPEED, 0)
        if keys_pressed[39] and x2 < WIDTH:  # Стрелка вправо
            canvas.move(paddle_b, PADDLE_SPEED, 0)

        check_ball_collision()

    root.after(20, move_paddles)

# Проверка столкновений
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
        ball_speed_x = BALL_SPEED
        ball_speed_y = 0
        ball_is_moving = True

def update_ball():
    global ball_speed_x, ball_speed_y, score_a, score_b, game_over
    
    if is_paused or game_over:
        root.after(20, update_ball)
        return
    
    if ball_is_moving:
        # Получаем текущие координаты шайбы
        x1, y1, x2, y2 = canvas.coords(ball)
        
        # Проверяем выход за границы поля и корректируем позицию
        if x1 < 0:
            x1 = 0
            x2 = x1 + 2 * BALL_RADIUS
            ball_speed_x *= -1
        if x2 > WIDTH:
            x2 = WIDTH
            x1 = x2 - 2 * BALL_RADIUS
            ball_speed_x *= -1
        if y1 < 0:
            y1 = 0
            y2 = y1 + 2 * BALL_RADIUS
            ball_speed_y *= -1
        if y2 > HEIGHT:
            y2 = HEIGHT
            y1 = y2 - 2 * BALL_RADIUS
            ball_speed_y *= -1
            
        # Устанавливаем скорректированные координаты
        canvas.coords(ball, x1, y1, x2, y2)
        
        # Проверка голов
        goal_width = 200
        goal_top = HEIGHT // 2 - goal_width // 2
        goal_bottom = HEIGHT // 2 + goal_width // 2
        
        # Проверяем, полностью ли шайба вошла в ворота
        if x1 <= 10 and y1 >= goal_top and y2 <= goal_bottom:
            score_b += 1
            reset_ball()
        elif x2 >= WIDTH - 10 and y1 >= goal_top and y2 <= goal_bottom:
            score_a += 1
            reset_ball()
        else:
            # Двигаем шайбу только если она не в воротах
            canvas.move(ball, ball_speed_x, ball_speed_y)

        # Обновляем счет
        canvas.itemconfig(score_text, text=f"Игрок Синий: {score_a}  Игрок Красный: {score_b}")

        if score_a >= WIN_SCORE or score_b >= WIN_SCORE:
            end_game()
    
    root.after(20, update_ball)
    
def reset_ball():
    global ball_speed_x, ball_speed_y, ball_is_moving
    canvas.coords(ball, 
                 WIDTH // 2 - BALL_RADIUS, 
                 HEIGHT // 2 - BALL_RADIUS, 
                 WIDTH // 2 + BALL_RADIUS, 
                 HEIGHT // 2 + BALL_RADIUS)
    ball_speed_x = 0
    ball_speed_y = 0
    ball_is_moving = False

def end_game():
    global game_over, end_menu
    
    game_over = True
    winner = "Игрок Синий" if score_a >= WIN_SCORE else "Игрок Красный"
    
    end_menu = Frame(root, bg="black", padx=40, pady=30)
    Label(end_menu, text=f"{winner} победил!", font=("Arial", 36, 'bold'), 
         bg="black", fg="white").pack(pady=15)
    
    Button(end_menu, text="Заново", font=("Arial", 24), 
          command=lambda: [end_menu.destroy(), restart_game()], 
          bg="#333", fg="white", width=15).pack(pady=10)
    Button(end_menu, text="Выход", font=("Arial", 24), 
          command=root.quit, bg="#333", fg="white", width=15).pack(pady=10)
    
    end_menu.place(relx=0.5, rely=0.5, anchor=CENTER)

# Инициализация и запуск игры
init_game()
reset_ball()
update_ball()
move_paddles()

root.mainloop()