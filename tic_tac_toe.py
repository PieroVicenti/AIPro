import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 350  # Increased height to accommodate reset button
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (0, 0, 0)  # Black background
LINE_COLOR = (255, 255, 255)  # White lines
CIRCLE_COLOR = (255, 255, 255)  # White circle
CROSS_COLOR = (255, 255, 255)  # White cross
WIN_COLOR = (0, 255, 0)  # Green lines for win
LOSE_COLOR = (255, 0, 0)  # Red lines for loss
DRAWCOLOR = (255, 255, 0)  # Red lines for loss
BUTTON_COLOR = (200, 200, 200)  # Light grey button
TEXT_COLOR = (50, 50, 50)  # Dark grey text

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Fonts
font = pygame.font.Font(None, 40)

# Board setup
board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines(color=LINE_COLOR):
    # Horizontal lines
    pygame.draw.line(screen, color, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, color, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, color, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)
    pygame.draw.line(screen, color, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return not np.any(board == 0)

def check_win(player):
    # Check vertical win
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Check horizontal win
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Check diagonal win
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

def minimax(board, depth, is_maximizing):
    # Check if there is a winner or the game is a draw
    if check_win(2):  # AI wins
        return 1
    if check_win(1):  # Player wins
        return -1
    if is_board_full():  # Draw
        return 0

    if is_maximizing:
        best_score = -np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -np.inf
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:  # Check if a move is possible
        mark_square(best_move[0], best_move[1], 2)

def draw_reset_button():
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 310, 200, 40))
    text = font.render("Reset", True, TEXT_COLOR)
    screen.blit(text, (120, 320))

def reset_game():
    global board, player, game_over
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    player = 1
    game_over = False
    screen.fill(BG_COLOR)  # Clear the screen
    draw_lines()
    draw_reset_button()  # Draw the reset button after clearing the screen

# Main loop
draw_lines()
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]  # x coordinate
            mouseY = event.pos[1]  # y coordinate

            if 50 <= mouseX <= 250 and 310 <= mouseY <= 350:  # Reset button click
                reset_game()
            
            if not game_over and mouseY < HEIGHT - 50:  # Ensure clicks are on the board
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    draw_figures()

                    if check_win(player):
                        draw_lines(WIN_COLOR if player == 1 else LOSE_COLOR)
                        draw_figures()  # Redraw figures after coloring the lines
                        print('Human wins!' if player == 1 else 'AI wins!')
                        game_over = True

                    player = 2 if player == 1 else 1

        if player == 2 and not game_over:
            ai_move()
            draw_figures()

            if check_win(player):
                draw_lines(LOSE_COLOR)
                draw_figures()  # Redraw figures after coloring the lines
                print('AI wins!')
                game_over = True

            player = 1

        if is_board_full() and not game_over:
            print('Draw!')
            game_over = True
            draw_lines(DRAWCOLOR)  # Keep the lines white even after the draw
            draw_figures()  # Ensure the figures stay visible

    draw_reset_button()
    pygame.display.update()
    
# Properly exit the game
pygame.quit()
exit()