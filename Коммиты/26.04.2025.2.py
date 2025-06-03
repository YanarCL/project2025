from tkinter import *
from PIL import Image, ImageTk
import math

# Создание основного окна
root = Tk()
root.title('Аэрохоккей')
root.attributes('-fullscreen', True)
root.resizable(False, False)

# Загрузка изображений
def load_image(image_path, size=None):
    try:
        image = Image.open(image_path)
        if size:
            image = image.resize(size)
        else:
            image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

# Загрузка всех изображений
bg_images = {
    'main_menu': load_image('D:\MainMenu.png'),
    'background': load_image('D:\FonForPlay.png'),
    'game_bg': load_image('D:\GameFone.png', (1000, 500))
}

# Основной фон
main_bg_label = Label(root)
main_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Настройки игры
WIDTH, HEIGHT = 1000, 500
PADDLE_RADIUS, BALL_RADIUS = 30, 15
PADDLE_SPEED, BALL_SPEED = 8, 14
WIN_SCORE = 4

# Игровые элементы
game = {
    'canvas': None,
    'paddle_a': None,
    'paddle_b': None,
    'ball': None,
    'score_text': None,
    'score_a': 0,
    'score_b': 0,
    'ball_speed_x': 0,
    'ball_speed_y': 0,
    'ball_is_moving': False,
    'is_paused': False,
    'game_over': False,
    'keys_pressed': {
        87: False, 65: False, 83: False, 68: False,  # WASD
        38: False, 40: False, 37: False, 39: False,  # Стрелки
        32: False  # Пробел
    },
    'pause_menu': None,
    'end_menu': None
}

# Главное меню
def show_main_menu():
    clear_game()
    main_bg_label.config(image=bg_images['main_menu'])
    start_btn.place(relx=0.5, rely=0.5, anchor='center')
    exit_btn.place(relx=0.5, rely=0.65, anchor='center')
    main_menu_btn.place_forget()

# Меню выбора режима
def show_game_menu():
    main_bg_label.config(image=bg_images['background'])
    start_btn.place_forget()
    exit_btn.place_forget()
    create_mode_buttons()
    main_menu_btn.place(relx=0.5, rely=0.9, anchor='center')

# Кнопки режимов игры
mode_buttons = []

def create_mode_buttons():
    clear_mode_buttons()
    
    buttons = [
        ('ОБУЧЕНИЕ', open_tutorial),
        ('ИГРА ПРОТИВ КОМПЬЮТЕРА', None),
        ('ИГРА ПРОТИВ ИГРОКА', start_game)
    ]
    
    for i, (text, command) in enumerate(buttons):
        btn = Button(root, text=text, width=30, height=2, bg='#080675', 
                    fg='#AFD7FF', font=('impact', 16), command=command)
        btn.place(relx=0.5, y=150 + i*120, anchor='center')
        mode_buttons.append(btn)

def clear_mode_buttons():
    for btn in mode_buttons:
        btn.destroy()
    mode_buttons.clear()

# Окно обучения
def open_tutorial():
    win = Toplevel(root)
    win.title("Обучение")
    win.geometry("800x400")
    
    text = """Правила игры:
    1. Управление:
       - Игрок 1: WASD
       - Игрок 2: Стрелки
       - Пробел: Пауза
    2. Цель: забить 5 шайб в ворота соперника
    3. Игра продолжается до 5 очков"""
    
    Label(win, text=text, font=('Arial', 14), justify=LEFT).pack(pady=20)
    Button(win, text="Закрыть", command=win.destroy, font=('Arial', 12)).pack()

# Игровая логика
def start_game():
    # Устанавливаем фон основного окна
    main_bg_label.config(image=bg_images['background'])
    
    clear_mode_buttons()
    main_menu_btn.place_forget()
    
    # Создаем игровое поле
    game['canvas'] = Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
    game['canvas'].place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Устанавливаем фон игрового поля
    if 'game_bg' in bg_images:
        game['canvas'].create_image(0, 0, anchor=NW, image=bg_images['game_bg'])
    
    init_game()
    reset_ball()
    create_pause_menu()
    
    root.bind("<KeyPress>", key_pressed)
    root.bind("<KeyRelease>", key_released)
    
    update_ball()
    move_paddles()

def init_game():
    # Счет
    game['score_text'] = game['canvas'].create_text(
        WIDTH//2, 30, 
        text="Игрок Синий: 0  Игрок Красный: 0", 
        font=("Arial", 24), fill="white"
    )
    
    # Биты
    game['paddle_a'] = game['canvas'].create_oval(
        WIDTH//4 - PADDLE_RADIUS, HEIGHT//2 - PADDLE_RADIUS,
        WIDTH//4 + PADDLE_RADIUS, HEIGHT//2 + PADDLE_RADIUS,
        fill="blue", outline="white"
    )
    
    game['paddle_b'] = game['canvas'].create_oval(
        3*WIDTH//4 - PADDLE_RADIUS, HEIGHT//2 - PADDLE_RADIUS,
        3*WIDTH//4 + PADDLE_RADIUS, HEIGHT//2 + PADDLE_RADIUS,
        fill="red", outline="white"
    )
    
    # Шайба
    game['ball'] = game['canvas'].create_oval(
        WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS,
        WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS,
        fill="white", outline="black"
    )
    
    # Ворота и разметка
    goal_width = 150
    game['canvas'].create_rectangle(
        0, HEIGHT//2 - goal_width//2, 10, HEIGHT//2 + goal_width//2,
        fill="gray", outline="white"
    )
    game['canvas'].create_rectangle(
        WIDTH-10, HEIGHT//2 - goal_width//2, WIDTH, HEIGHT//2 + goal_width//2,
        fill="gray", outline="white"
    )
    game['canvas'].create_line(WIDTH//2, 0, WIDTH//2, HEIGHT, fill="white", dash=(5,5))
    game['canvas'].create_rectangle(0, 0, WIDTH, HEIGHT, outline="white", width=3)

def reset_ball():
    game['canvas'].coords(game['ball'],
        WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS,
        WIDTH//2 + BALL_RADIUS, HEIGHT//2 + BALL_RADIUS
    )
    game['ball_speed_x'] = 0
    game['ball_speed_y'] = 0
    game['ball_is_moving'] = False

def restart_game():
    game['score_a'] = 0
    game['score_b'] = 0
    game['ball_is_moving'] = False
    game['is_paused'] = False
    game['game_over'] = False
    
    hide_pause_menu()
    if game['end_menu']:
        game['end_menu'].destroy()
        game['end_menu'] = None
    
    game['canvas'].delete("all")
    if 'game_bg' in bg_images:
        game['canvas'].create_image(0, 0, anchor=NW, image=bg_images['game_bg'])
    
    init_game()
    reset_ball()

# Меню паузы
def create_pause_menu():
    game['pause_menu'] = Frame(root, bg='black', padx=30, pady=20)
    
    Label(game['pause_menu'], text="ПАУЗА", font=('Arial', 36, 'bold'), 
          fg='white', bg='black').pack(pady=10)
    
    buttons = [
        ("Продолжить", toggle_pause),
        ("Заново", restart_game),
        ("В меню", return_to_menu)
    ]
    
    for text, cmd in buttons:
        Button(game['pause_menu'], text=text, font=('Arial', 18), width=12,
              command=cmd, bg='#333', fg='white').pack(pady=5)

def show_pause_menu():
    if game['pause_menu']:
        game['pause_menu'].place(relx=0.5, rely=0.5, anchor=CENTER)

def hide_pause_menu():
    if game['pause_menu']:
        game['pause_menu'].place_forget()

def toggle_pause():
    if not game['game_over']:
        game['is_paused'] = not game['is_paused']
        if game['is_paused']:
            show_pause_menu()
        else:
            hide_pause_menu()

# Управление
def key_pressed(event):
    if event.keycode in game['keys_pressed']:
        game['keys_pressed'][event.keycode] = True
    if event.keycode == 32:  # Пробел
        toggle_pause()

def key_released(event):
    if event.keycode in game['keys_pressed']:
        game['keys_pressed'][event.keycode] = False

def move_paddles():
    if not game['is_paused'] and not game['game_over']:
        # Игрок 1 (WASD)
        x1, y1, x2, y2 = game['canvas'].coords(game['paddle_a'])
        if game['keys_pressed'][87] and y1 > 0:  # W
            game['canvas'].move(game['paddle_a'], 0, -PADDLE_SPEED)
        if game['keys_pressed'][83] and y2 < HEIGHT:  # S
            game['canvas'].move(game['paddle_a'], 0, PADDLE_SPEED)
        if game['keys_pressed'][65] and x1 > 0:  # A
            game['canvas'].move(game['paddle_a'], -PADDLE_SPEED, 0)
        if game['keys_pressed'][68] and x2 < WIDTH//2:  # D
            game['canvas'].move(game['paddle_a'], PADDLE_SPEED, 0)

        # Игрок 2 (Стрелки)
        x1, y1, x2, y2 = game['canvas'].coords(game['paddle_b'])
        if game['keys_pressed'][38] and y1 > 0:  # Вверх
            game['canvas'].move(game['paddle_b'], 0, -PADDLE_SPEED)
        if game['keys_pressed'][40] and y2 < HEIGHT:  # Вниз
            game['canvas'].move(game['paddle_b'], 0, PADDLE_SPEED)
        if game['keys_pressed'][37] and x1 > WIDTH//2:  # Влево
            game['canvas'].move(game['paddle_b'], -PADDLE_SPEED, 0)
        if game['keys_pressed'][39] and x2 < WIDTH:  # Вправо
            game['canvas'].move(game['paddle_b'], PADDLE_SPEED, 0)

        check_collision()

    root.after(20, move_paddles)

def check_collision():
    ball_coords = game['canvas'].coords(game['ball'])
    paddle_a_coords = game['canvas'].coords(game['paddle_a'])
    paddle_b_coords = game['canvas'].coords(game['paddle_b'])

    # Столкновение с битой A
    if (ball_coords[0] <= paddle_a_coords[2] and ball_coords[2] >= paddle_a_coords[0] and
        ball_coords[1] <= paddle_a_coords[3] and ball_coords[3] >= paddle_a_coords[1]):
        handle_collision(paddle_a_coords, ball_coords)

    # Столкновение с битой B
    if (ball_coords[0] <= paddle_b_coords[2] and ball_coords[2] >= paddle_b_coords[0] and
        ball_coords[1] <= paddle_b_coords[3] and ball_coords[3] >= paddle_b_coords[1]):
        handle_collision(paddle_b_coords, ball_coords)

def handle_collision(paddle_coords, ball_coords):
    if not game['ball_is_moving']:
        game['ball_is_moving'] = True
        game['ball_speed_x'] = BALL_SPEED * (1 if paddle_coords[0] < WIDTH//2 else -1)
        game['ball_speed_y'] = 0
        return
    
    paddle_center = ((paddle_coords[0]+paddle_coords[2])/2, (paddle_coords[1]+paddle_coords[3])/2)
    ball_center = ((ball_coords[0]+ball_coords[2])/2, (ball_coords[1]+ball_coords[3])/2)
    
    dx = ball_center[0] - paddle_center[0]
    dy = ball_center[1] - paddle_center[1]
    
    distance = max(math.sqrt(dx*dx + dy*dy), 0.1)
    dx /= distance
    dy /= distance
    
    game['ball_speed_x'] = BALL_SPEED * dx
    game['ball_speed_y'] = BALL_SPEED * dy
    
    # Коррекция позиции чтобы не залипали
    overlap = PADDLE_RADIUS + BALL_RADIUS - distance + 2
    game['canvas'].move(game['ball'], dx*overlap, dy*overlap)

def update_ball():
    if game['is_paused'] or game['game_over']:
        root.after(20, update_ball)
        return
    
    if game['ball_is_moving']:
        x1, y1, x2, y2 = game['canvas'].coords(game['ball'])
        
        # Отскок от стен
        if y1 <= 0 or y2 >= HEIGHT:
            game['ball_speed_y'] *= -1
        if x1 <= 0 or x2 >= WIDTH:
            game['ball_speed_x'] *= -1
            
        # Проверка голов
        goal_width = 150
        goal_top = HEIGHT//2 - goal_width//2
        goal_bottom = HEIGHT//2 + goal_width//2
        
        if x1 <= 10 and goal_top <= y1 <= goal_bottom and goal_top <= y2 <= goal_bottom:
            game['score_b'] += 1
            update_score()
            reset_ball()
        elif x2 >= WIDTH-10 and goal_top <= y1 <= goal_bottom and goal_top <= y2 <= goal_bottom:
            game['score_a'] += 1
            update_score()
            reset_ball()
        else:
            game['canvas'].move(game['ball'], game['ball_speed_x'], game['ball_speed_y'])
        
        if game['score_a'] >= WIN_SCORE or game['score_b'] >= WIN_SCORE:
            end_game()
    
    root.after(20, update_ball)

def update_score():
    game['canvas'].itemconfig(game['score_text'],
        text=f"Игрок Синий: {game['score_a']}  Игрок Красный: {game['score_b']}")

def end_game():
    game['game_over'] = True
    
    winner = "Синий игрок" if game['score_a'] > game['score_b'] else "Красный игрок"
    
    game['end_menu'] = Frame(root, bg='black', padx=30, pady=20)
    Label(game['end_menu'], text=f"{winner} победил!", font=('Arial', 36, 'bold'),
          fg='white', bg='black').pack(pady=10)
    
    Button(game['end_menu'], text="Заново", font=('Arial', 18), width=12,
          command=restart_game, bg='#333', fg='white').pack(pady=5)
    Button(game['end_menu'], text="В меню", font=('Arial', 18), width=12,
          command=return_to_menu, bg='#333', fg='white').pack(pady=5)
    
    game['end_menu'].place(relx=0.5, rely=0.5, anchor=CENTER)

def return_to_menu():
    clear_game()
    show_game_menu()

def clear_game():
    if game['canvas']:
        game['canvas'].destroy()
        game['canvas'] = None
    if game['pause_menu']:
        game['pause_menu'].destroy()
        game['pause_menu'] = None
    if game['end_menu']:
        game['end_menu'].destroy()
        game['end_menu'] = None
    
    root.unbind("<KeyPress>")
    root.unbind("<KeyRelease>")
    
    main_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Создание интерфейса
start_btn = Button(root, text='Начать игру', width=20, height=2, bg='#080675',
                  fg='#AFD7FF', font=('impact', 16), command=show_game_menu)
exit_btn = Button(root, text='Выход', width=20, height=2, bg='#080675',
                 fg='#AFD7FF', font=('impact', 16), command=root.destroy)
main_menu_btn = Button(root, text='Главное меню', width=20, height=2, bg='#080675',
                      fg='#AFD7FF', font=('impact', 16), command=show_main_menu)

show_main_menu()
root.mainloop()