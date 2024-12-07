from tkinter import *
import random

GAME_WIDTH = 600
GAME_HEIGHT = 600
SNAKE_SPEED = 60
SPACE_SIZE = 20
BODY_NUM = 3
SNAKE_COLOR = "#800080"
FOOD_COLOR = "yellow"
BG_COLOR = "black"
GRID_COLOR = "gray"


class Snake:

    def __init__(self):
        self.body_size = BODY_NUM
        self.coordinates = []
        self.circles = []

        for i in range(0, BODY_NUM):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            circle = canvas.create_oval(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.circles.append(circle)


class Food:

    def __init__(self):

        x = random.randint(0, int(GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE,
                                y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def draw_grid():
    # Draw horizontal grid lines
    for y in range(0, GAME_HEIGHT, SPACE_SIZE):
        canvas.create_line(0, y, GAME_WIDTH, y, fill=GRID_COLOR)

    # Draw vertical grid lines
    for x in range(0, GAME_WIDTH, SPACE_SIZE):
        canvas.create_line(x, 0, x, GAME_HEIGHT, fill=GRID_COLOR)


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    circle = canvas.create_oval(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.circles.insert(0, circle)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]

        canvas.delete(snake.circles[-1])

        del snake.circles[-1]

    if check_collisons(snake):
        game_over()
    else:
        window.after(SNAKE_SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if (new_direction == 'left'):
        if (direction != 'right'):
            direction = new_direction
    elif (new_direction == 'right'):
        if (direction != 'left'):
            direction = new_direction
    elif (new_direction == 'up'):
        if (direction != 'down'):
            direction = new_direction
    elif (new_direction == 'down'):
        if (direction != 'up'):
            direction = new_direction


def check_collisons(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height()/2,
                       font=('roboto', 70), text="GAME OVER", fill="red", tag="game over")
    restart_button = Button(window, text="Restart",
                            command=restart_game, font=('consolas', 20))
    restart_button.place(x=0, y=0)


def restart_game():
    global snake, food, score, direction

    canvas.delete(ALL)
    draw_grid()
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)


window = Tk()
window.title("Snek Gaem")
window.iconbitmap("Snake Game\icon.ico")
window.resizable(False, False)

score = 0
direction = 'down'
label = Label(window, text="Score: {}".format(score), font=('lato', 40))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

draw_grid()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2)-(window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y -50}")

snake = Snake()
food = Food()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

next_turn(snake, food)


window.mainloop()
