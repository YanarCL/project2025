from tkinter import *
from tkinter import PhotoImage, Canvas
import random

# Пути к изображениям
BG_MAIN_PATH = "D:/2 курс/Практика 2 курс 2 семестр/MainMenu.png"
BG_START_PATH = "D:/2 курс/Практика 2 курс 2 семестр/Prik.png"
FONT = ("Comic Sans MS", 30)
FONT_HOVER = ("Comic Sans MS", 31, "bold")
BUTTON_BG = "#4fc8f3"
BUTTON_FG = "white"

# Основное окно
window = Tk()
window.resizable(False, False)
window.title("Игра Жизнь")
window.state('zoomed')

# Функция для центрирования окна
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

# Функции для кнопок
def on_enter(event):
    event.widget.config(font=FONT_HOVER)

def on_leave(event):
    event.widget.config(font=FONT)

def create_button(parent, text, command=None):
    button = Label(parent, text=text, fg=BUTTON_FG, font=FONT, cursor="hand2", relief="flat", bg=BUTTON_BG)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    if command:
        button.bind("<Button-1>", lambda event: command())
    return button

# Переключение между меню и игрой
def show_menu():
    game_frame.pack_forget()  # Скрываем игровое поле
    menu_frame.pack(fill="both", expand=True)  # Показываем меню
    game.stop()  # Останавливаем игру

def start_game():
    menu_frame.pack_forget()  # Скрываем меню
    game_frame.pack(fill="both", expand=True)  # Показываем игровое поле
    game.start()  # Запускаем игру

def exit_game():
    window.destroy()

# Окно с шаблонами
def pattern():
    pattern_window = Toplevel(window)
    pattern_window.resizable(False, False)
    pattern_window.title("Шаблоны")
    center_window(pattern_window, 1000, 500)
    pattern_window.bg3 = PhotoImage(file="D:/2 курс/Практика 2 курс 2 семестр/MainMenu.png")
    canvas1 = Canvas(pattern_window, width=1000, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=pattern_window.bg3, anchor="nw")
    close_button = create_button(pattern_window, "  Выход", pattern_window.destroy)
    canvas1.create_window(820, 430, anchor="nw", window=close_button)

# Окно с обучением
def open_tutorial():
    tutorial_window = Toplevel(window)
    tutorial_window.resizable(False, False)
    tutorial_window.title("Обучение")
    center_window(tutorial_window, 1000, 500)
    tutorial_window.bg2 = PhotoImage(file="D:/2 курс/Практика 2 курс 2 семестр/MainMenu.png")
    canvas1 = Canvas(tutorial_window, width=1000, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=tutorial_window.bg2, anchor="nw")
    button_exit_tut = create_button(tutorial_window, "Закрыть", tutorial_window.destroy)
    canvas1.create_window(820, 430, anchor="nw", window=button_exit_tut)
    tutorial_text = """
    Добро пожаловать в обучение по игре Жизнь!

    Цель игры:
    Это исследование динамики популяции клеток на двумерной решетке. 
    Игра была разработана математиком Джоном Конвеем в 1970 году и не является игрой 
    в традиционном смысле, а скорее симуляцией. 

    Правила:
    1. Клетки: Каждая клетка на решетке может быть "живой" или "мертвой".
    2. Соседство: Каждая клетка имеет восемь соседей (горизонтально, вертикально и по диагонали).
    3. Правила эволюции:
   • Если живая клетка имеет 2 или 3 живых соседа, она остается живой; иначе она умирает (от перенаселения или одиночества).
   • Если мертвая клетка имеет ровно 3 живых соседа, она становится живой (в результате размножения).

    Нажмите 'Закрыть', чтобы вернуться в игру.
    """
    label = Label(tutorial_window, text=tutorial_text, justify="left", padx=10, pady=10, font=('Comic Sans MS', 11), fg="white", bg="#4fc8f3")
    canvas1.create_window(500, 200, anchor="center", window=label)

# Класс игры "Жизнь"
class GameOfLife:
    def __init__(self, root, width=50, height=50, cell_size=10):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(width)] for _ in range(height)]  # Начинаем с пустой сетки
        self.canvas = Canvas(root, width=width*cell_size, height=height*cell_size)
        self.canvas.pack()
        self.running = False
        self.draw_grid()
        self.create_buttons()
        self.canvas.bind("<Button-1>", self.toggle_cell)  # Обработчик клика мыши

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="green"
                    )
                else:
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="white", outline="gray"
                    )

    def create_buttons(self):
        self.start_button = Button(self.root, text="Start", command=self.start)
        self.start_button.pack(side=LEFT)
        self.stop_button = Button(self.root, text="Stop", command=self.stop)
        self.stop_button.pack(side=LEFT)
        self.reset_button = Button(self.root, text="Reset", command=self.reset)
        self.reset_button.pack(side=LEFT)
        self.randomize_button = Button(self.root, text="Randomize", command=self.randomize)
        self.randomize_button.pack(side=LEFT)

    def start(self):
        self.running = True
        self.run_generation()

    def stop(self):
        self.running = False

    def reset(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]  # Очистка сетки
        self.draw_grid()

    def randomize(self):
        self.grid = [[random.choice([0, 1]) for _ in range(self.width)] for _ in range(self.height)]
        self.draw_grid()

    def run_generation(self):
        if not self.running:
            return
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                if self.grid[y][x]:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y][x] = 0
                    else:
                        new_grid[y][x] = 1
                else:
                    if neighbors == 3:
                        new_grid[y][x] = 1
        self.grid = new_grid
        self.draw_grid()
        self.root.after(100, self.run_generation)

    def count_neighbors(self, x, y):
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors += self.grid[ny][nx]
        return neighbors

    def toggle_cell(self, event):
        # Определяем, по какой клетке кликнули
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1 - self.grid[y][x]  # Переключаем состояние клетки
            self.draw_grid()

# Меню
menu_frame = Frame(window)
menu_frame.pack(fill="both", expand=True)

bg_main = PhotoImage(file=BG_MAIN_PATH)
canvas = Canvas(menu_frame, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_main, anchor="nw")
canvas.create_text(770, 150, text="Жизнь", font=("Comic Sans MS", 60, "bold"), fill="white")

button_start = create_button(menu_frame, "  Начать", start_game)
button_exit = create_button(menu_frame, "  Выход",
exit_game)
button_pattern = create_button(menu_frame, "Шаблоны", pattern)
button_music = create_button(menu_frame, "♫")
button_info = create_button(menu_frame, "🛈", open_tutorial)

canvas.create_window(670, 230, anchor="nw", window=button_start)
canvas.create_window(678, 370, anchor="nw", window=button_exit)
canvas.create_window(670, 300, anchor="nw", window=button_pattern)
canvas.create_window(12, 2, anchor="nw", window=button_music)
canvas.create_window(1485, 2, anchor="nw", window=button_info)

# Игровое поле
game_frame = Frame(window)

bg_start = PhotoImage(file=BG_START_PATH)
game_canvas = Canvas(game_frame, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
game_canvas.pack(fill="both", expand=True)
game_canvas.create_image(0, 0, image=bg_start, anchor="nw")

button_menu = create_button(game_frame, "Меню", show_menu)
game_canvas.create_window(12, 2, anchor="nw", window=button_menu)

# Создаем игру
game = GameOfLife(game_canvas)

# Запуск основного цикла
window.mainloop()