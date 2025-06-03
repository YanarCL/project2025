from tkinter import *
from PIL import Image, ImageTk
import random

# Настройки игры
WIDTH = 1000
HEIGHT = 800
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 20
BALL_RADIUS = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WIN_SCORE = 10

# Инициализация окна
root = Tk()
root.title('Аэрохоккей')
root.geometry(f'{WIDTH}x{HEIGHT}')

# Глобальные переменные
mode_buttons = []  # Инициализация переменной mode_buttons

def load_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((WIDTH, HEIGHT))
        return image
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

# Загрузка изображения для главного экрана
main_menu_photo = load_image('D:/2 курс/Практика 2 курс 2 семестр/MainMenu.png')
if main_menu_photo:
    main_menu_photo = ImageTk.PhotoImage(main_menu_photo)

# Загрузка изображения для второго экрана
second_screen_photo = load_image('D:/2 курс/Практика 2 курс 2 семестр/MainMenu.png')
if second_screen_photo:
    second_screen_photo = ImageTk.PhotoImage(second_screen_photo)

# Создание Label для отображения изображений
label = Label(root)
label.pack()

# Создание Canvas для игры
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

def show_main_menu():
    label.config(image=main_menu_photo)
    label.image = main_menu_photo
    btn.place(relx=0.5, rely=0.4, anchor='center')  # Кнопка "Начать играть"
    exit_btn_main.place(relx=0.5, rely=0.55, anchor='center')  # Кнопка "Выход"
    clear_mode_buttons()
    exit_btn.place_forget()

def change_image():
    label.config(image=second_screen_photo)
    label.image = second_screen_photo
    btn.place_forget()
    exit_btn_main.place_forget()  # Скрываем кнопку выхода на главном экране
    create_game_mode_buttons()
    exit_btn.place(relx=0.95, rely=0.95, anchor='se')

def create_game_mode_buttons():
    global mode_buttons
    training_button = Button(root, text='ОБУЧЕНИЕ', width=35, height=1, font=('Comic Sans MS', 20, 'bold'),
                             command=open_tutorial, bg='white', fg='black', bd=0)
    training_button.place(relx=0.5, y=100, anchor='center')
    mode_buttons.append(training_button)

    vs_computer_button = Button(root, text='ИГРА ПРОТИВ КОМПЬЮТЕРА', width=35, height=2, font=('Comic Sans MS', 20, 'bold'),
                                bg='white', fg='black', bd=0, command=start_vs_computer)
    vs_computer_button.place(relx=0.5, y=250, anchor='center')
    mode_buttons.append(vs_computer_button)

    vs_player_button = Button(root, text='ИГРА ПРОТИВ ИГРОКА', width=35, height=2, font=('Comic Sans MS', 20, 'bold'),
                              bg='white', fg='black', bd=0, command=start_vs_player)
    vs_player_button.place(relx=0.5, y=400, anchor='center')
    mode_buttons.append(vs_player_button)

def exit_game():
    show_main_menu()  # Возвращаемся на главный экран

def clear_mode_buttons():
    global mode_buttons
    for button in mode_buttons:
        button.destroy()
    mode_buttons = []

def open_tutorial():
    tutorial_window = Toplevel(root)
    tutorial_window.title("Обучение")
    tutorial_window.geometry('800x300')

    tutorial_text = """
    Добро пожаловать в обучение по игре Аэрохоккей!

    Цель игры:
    Забейте как можно большее количество шайб в ворота противника и не дайте ему забить в свои.
    Победа засчитывается в случае набора одной из сторон десяти очков.

    Правила:
    1. Управляйте битой с помощью мыши (в режиме против компьютера) или клавиш WASD и стрелок (в режиме против игрока).
    2. Шайба отскакивает от стен и бит.
    3. Игра заканчивается, когда один из игроков набирает 10 очков.

    Нажмите 'Закрыть', чтобы вернуться в игру.
    """

    label = Label(tutorial_window, text=tutorial_text, justify="left", padx=10, pady=10, font=('Arial', 10))
    label.pack()

    close_button = Button(tutorial_window, text='Закрыть', command=tutorial_window.destroy, font=('Arial', 12))
    close_button.pack(pady=10)

# Игровые элементы
paddle_a = None
paddle_b = None
ball = None
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y
score_a = 0
score_b = 0
score_label = Label(root, text=f"Игрок A: {score_a}  Игрок B: {score_b}", font=("Arial", 20), fg="white", bg="black")

# Управление битами
def move_paddle_a(event):
    x = event.x
    canvas.coords(paddle_a, x - PADDLE_WIDTH // 2, 10, x + PADDLE_WIDTH // 2, 10 + PADDLE_HEIGHT)

def move_paddle_a_wasd(event):
    x1, y1, x2, y2 = canvas.coords(paddle_a)
    if event.keysym == 'a' and x1 > 0:
        canvas.move(paddle_a, -20, 0)
    elif event.keysym == 'd' and x2 < WIDTH:
        canvas.move(paddle_a, 20, 0)

def move_paddle_b_arrows(event):
    x1, y1, x2, y2 = canvas.coords(paddle_b)
    if event.keysym == 'Left' and x1 > 0:
        canvas.move(paddle_b, -20, 0)
    elif event.keysym == 'Right' and x2 < WIDTH:
        canvas.move(paddle_b, 20, 0)

# Логика игры
def update_ball():
    global ball_speed_x, ball_speed_y, score_a, score_b

    # Движение шайбы
    canvas.move(ball, ball_speed_x, ball_speed_y)
    x1, y1, x2, y2 = canvas.coords(ball)

    # Отскок от стен
    if x1 <= 0 or x2 >= WIDTH:
        ball_speed_x = -ball_speed_x
    if y1 <= 0 or y2 >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Отскок от бит
    paddle_a_coords = canvas.coords(paddle_a)
    paddle_b_coords = canvas.coords(paddle_b)

    if (y1 <= paddle_a_coords[3] and x1 >= paddle_a_coords[0] and x2 <= paddle_a_coords[2]):
        ball_speed_y = -ball_speed_y
    if (y2 >= paddle_b_coords[1] and x1 >= paddle_b_coords[0] and x2 <= paddle_b_coords[2]):
        ball_speed_y = -ball_speed_y

    # Голы
    if y1 <= 0:
        score_b += 1
        reset_ball()
    if y2 >= HEIGHT:
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
    global ball_speed_x, ball_speed_y
    canvas.coords(ball, WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS)
    ball_speed_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
    ball_speed_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

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

# Режим игры против компьютера
def start_vs_computer():
    global paddle_a, paddle_b, ball, score_a, score_b, canvas
    canvas.delete("all")
    score_a = 0
    score_b = 0
    score_label.config(text=f"Игрок A: {score_a}  Игрок B: {score_b}")
    paddle_a = canvas.create_rectangle(WIDTH // 2 - PADDLE_WIDTH // 2, 10, WIDTH // 2 + PADDLE_WIDTH // 2, 10 + PADDLE_HEIGHT, fill="blue")
    paddle_b = canvas.create_rectangle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 10 - PADDLE_HEIGHT, WIDTH // 2 + PADDLE_WIDTH // 2, HEIGHT - 10, fill="red")
    ball = canvas.create_oval(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS, fill="white")
    reset_ball()
    root.bind("<Motion>", move_paddle_a)  # Управление мышкой
    update_ball()

# Режим игры против игрока
def start_vs_player():
    global paddle_a, paddle_b, ball, score_a, score_b, canvas
    canvas.delete("all")
    score_a = 0
    score_b = 0
    score_label.config(text=f"Игрок A: {score_a}  Игрок B: {score_b}")
    paddle_a = canvas.create_rectangle(WIDTH // 2 - PADDLE_WIDTH // 2, 10, WIDTH // 2 + PADDLE_WIDTH // 2, 10 + PADDLE_HEIGHT, fill="blue")
    paddle_b = canvas.create_rectangle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 10 - PADDLE_HEIGHT, WIDTH // 2 + PADDLE_WIDTH // 2, HEIGHT - 10, fill="red")
    ball = canvas.create_oval(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS, fill="white")
    reset_ball()
    root.bind("<KeyPress>", move_paddle_a_wasd)  # Управление WASD
    root.bind("<KeyPress>", move_paddle_b_arrows)  # Управление стрелками
    update_ball()

# Кнопка "Начать играть" (прозрачная)
btn = Button(root, text='Начать играть', font=('Comic Sans MS', 20, 'bold'), 
             bg='SystemButtonFace', fg='black', bd=0, command=change_image, width=20, height=1)

# Кнопка "Выход" на главном экране (прозрачная)
exit_btn_main = Button(root, text='Выход', font=('Comic Sans MS', 20, 'bold'), 
                       bg='SystemButtonFace', fg='black', bd=0, command=root.destroy, width=20, height=1)

# Кнопка "Выход" на втором экране
exit_btn = Button(root, text='Выход', bg='red', fg='white', font=('Comic Sans MS', 15), command=exit_game)
exit_btn.place_forget()

# Показываем главный экран при запуске
show_main_menu()

root.mainloop()