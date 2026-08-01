import random
import turtle


wins = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def check_win(board, player):
    for a, b, c in wins:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def get_winning_line(board, player):
    for a, b, c in wins:
        if board[a] == board[b] == board[c] == player:
            return a, b, c
    return None


def check_draw(board):
    return all(box in ["X", "O"] for box in board)


def computer_move(board, difficulty):
    available_moves = []

    for i, box in enumerate(board):
        if box not in ["X", "O"]:
            available_moves.append(i)

    if not available_moves:
        return None

    if difficulty == "easy":
        return random.choice(available_moves)

    if difficulty == "medium":
        for move in available_moves:
            temp_board = board[:]
            temp_board[move] = "O"
            if check_win(temp_board, "O"):
                return move

        for move in available_moves:
            temp_board = board[:]
            temp_board[move] = "X"
            if check_win(temp_board, "X"):
                return move

        return random.choice(available_moves)

    


screen = turtle.Screen()
screen.setup(600, 600)
screen.title("Tic Tac Toe")
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.color("white")
pen.pensize(5)

text_pen = turtle.Turtle()
text_pen.speed(0)
text_pen.hideturtle()
text_pen.color("white")

board = ["", "", "", "", "", "", "", "", ""]
current_player = "X"
game_mode = None
difficulty = "medium"
game_over = False
screen_name = "start"


def clear_screen():
    pen.clear()
    text_pen.clear()


def write_text(message, x, y, size=22, align="center"):
    text_pen.penup()
    text_pen.goto(x, y)
    text_pen.write(message, align=align, font=("Arial", size, "normal"))


def draw_line(x1, y1, x2, y2):
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.goto(x2, y2)


def draw_button(label, x1, y1, x2, y2):
    pen.color("white")
    pen.pensize(3)
    draw_line(x1, y1, x2, y1)
    draw_line(x2, y1, x2, y2)
    draw_line(x2, y2, x1, y2)
    draw_line(x1, y2, x1, y1)
    write_text(label, (x1 + x2) / 2, (y1 + y2) / 2 - 12, 18)


def draw_start_screen():
    global screen_name

    screen_name = "start"
    clear_screen()
    write_text("Tic Tac Toe", 0, 145, 34)
    write_text("Choose a game mode", 0, 95, 18)
    draw_button("PvP", -180, 10, -20, -70)
    draw_button("Computer", 20, 10, 180, -70)


def draw_difficulty_screen():
    global screen_name

    screen_name = "difficulty"
    clear_screen()
    write_text("Choose difficulty", 0, 125, 30)
    write_text("Computer will play as O", 0, 80, 16)
    draw_button("Easy", -180, 0, -20, -80)
    draw_button("Medium", 20, 0, 180, -80)


def draw_board():
    clear_screen()
    write_text("Click a square to add your move", 0, 205, 18)

    pen.color("white")
    pen.pensize(5)

    draw_line(-50, 150, -50, -150)
    draw_line(50, 150, 50, -150)
    draw_line(-150, 50, 150, 50)
    draw_line(-150, -50, 150, -50)


def draw_x(x, y):
    pen.color("white")
    pen.pensize(10)

    pen.penup()
    pen.goto(x - 30, y + 30)
    pen.pendown()
    pen.goto(x + 30, y - 30)

    pen.penup()
    pen.goto(x + 30, y + 30)
    pen.pendown()
    pen.goto(x - 30, y - 30)


def draw_o(x, y):
    radius = 35

    pen.color("white")
    pen.pensize(10)

    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.circle(radius)


def get_square(x, y):
    if x < -150 or x > 150 or y < -150 or y > 150:
        return None

    if x < -50:
        col = 0
        center_x = -100
    elif x < 50:
        col = 1
        center_x = 0
    else:
        col = 2
        center_x = 100

    if y > 50:
        row = 0
        center_y = 100
    elif y > -50:
        row = 1
        center_y = 0
    else:
        row = 2
        center_y = -100

    index = row * 3 + col
    return index, (center_x, center_y)


def get_center_from_index(index):
    row = index // 3
    col = index % 3
    center_x = -100 + col * 100
    center_y = 100 - row * 100
    return center_x, center_y


def start_game(selected_mode, selected_difficulty=None):
    global board, current_player, game_mode, difficulty, game_over, screen_name

    board = ["", "", "", "", "", "", "", "", ""]
    current_player = "X"
    game_mode = selected_mode
    if selected_difficulty is not None:
        difficulty = selected_difficulty
    game_over = False
    screen_name = "game"
    draw_board()


def end_game(message):
    global game_over

    game_over = True
    text_pen.clear()
    write_text(message, 0, 210, 20)
    write_text("Click anywhere to return to the menu", 0, -215, 14)


def place_move(index, player):
    board[index] = player
    center_x, center_y = get_center_from_index(index)

    if player == "X":
        draw_x(center_x, center_y)
    else:
        draw_o(center_x, center_y)


def draw_winning_line(line):
    start_index = line[0]
    end_index = line[2]

    start_x, start_y = get_center_from_index(start_index)
    end_x, end_y = get_center_from_index(end_index)

    pen.color("red")
    pen.pensize(8)
    draw_line(start_x, start_y, end_x, end_y)


def check_game_finished(player):
    winning_line = get_winning_line(board, player)

    if winning_line is not None:
        draw_winning_line(winning_line)
        end_game(f"{player} won the game")
        return True

    if check_draw(board):
        end_game("It's a draw")
        return True

    return False


def make_computer_move():
    if game_over:
        return

    move = computer_move(board, difficulty)

    if move is None:
        return

    place_move(move, "O")
    check_game_finished("O")


def handle_start_click(x, y):
    if -180 <= x <= -20 and -70 <= y <= 10:
        start_game("pvp")
    elif 20 <= x <= 180 and -70 <= y <= 10:
        draw_difficulty_screen()


def handle_difficulty_click(x, y):
    if -180 <= x <= -20 and -80 <= y <= 0:
        start_game("computer", "easy")
    elif 20 <= x <= 180 and -80 <= y <= 0:
        start_game("computer", "medium")


def handle_game_click(x, y):
    global current_player

    if game_over:
        draw_start_screen()
        return

    square = get_square(x, y)

    if square is None:
        return

    index, center = square

    if board[index] != "":
        return

    if game_mode == "pvp":
        place_move(index, current_player)

        if check_game_finished(current_player):
            return

        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

    elif game_mode == "computer":
        place_move(index, "X")

        if check_game_finished("X"):
            return

        screen.ontimer(make_computer_move, 300)


def handle_click(x, y):
    if screen_name == "start":
        handle_start_click(x, y)
    elif screen_name == "difficulty":
        handle_difficulty_click(x, y)
    elif screen_name == "game":
        handle_game_click(x, y)


draw_start_screen()
screen.onclick(handle_click)
screen.mainloop()
