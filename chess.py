#   _______     _______          __  __ ______
#  |  __ \ \   / / ____|   /\   |  \/  |  ____|
#  | |__) \ \_/ / |  __   /  \  | \  / | |__
#  |  ___/ \   /| | |_ | / /\ \ | |\/| |  __|
#  | |      | | | |__| |/ ____ \| |  | | |____
#  |_|____ _|_| _\_____/_/____\_\_|__|_|______|
#   / ____| |  | |  ____|/ ____/ ____|
#  | |    | |__| | |__  | (___| (___
#  | |    |  __  |  __|  \___ \\___ \
#  | |____| |  | | |____ ____) |___) |
#   \_____|_|  |_|______|_____/_____/
#
# by paz
#
# pieces textures from: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
from piece_logic import *

# initialize pygame
pygame.init()

# screen
width, height = 640 + 240, 640
screen = pygame.display.set_mode((width, height))


# title & icon of window
pygame.display.set_caption("Chess...")
icon = pygame.image.load("piece_textures/wk.png")
pygame.display.set_icon(icon)

# colors
BLACK_SQUARES_COLOR = (29, 120, 115)
WHITE_SQUARES_COLOR = (103, 146, 137)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BACKGROUND = (7, 30, 34)
BLUE = (202, 228, 241)
TEXT_COLOR = 244, 192, 149

# text
font = pygame.font.SysFont("Aerial", 32)
white_turn = font.render("White's turn", True, WHITE)
black_turn = font.render("Black's turn", True, WHITE)
white_check = font.render("White is in check", True, WHITE)
black_check = font.render("Black is in check", True, WHITE)
promote = font.render("Promote to: ", True, WHITE)

font = pygame.font.SysFont("Aerial", 36)
checkmate = font.render("Checkmate!", True, WHITE)
white_won = font.render("White won by", True, WHITE)
black_won = font.render("Black won by", True, WHITE)
stalemate = font.render("Draw by Stalemate!", True, WHITE)
no_pieces1 = font.render("Draw by no", True, WHITE)
no_pieces2 = font.render("pieces to", True, WHITE)
no_pieces3 = font.render("checkamte!", True, WHITE)


# reset button
reset_image = pygame.image.load("reset.png")


starting_board = [  # starting position
     ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
     ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
     ["", "", "", "", "", "", "", ""],
     ["", "", "", "", "", "", "", ""],
     ["", "", "", "", "", "", "", ""],
     ["", "", "", "", "", "", "", ""],
     ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
     ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
 ]
# starting_board = [  # starting position
#    ["", "", "", "", "bk", "", "", ""],
#    ["", "", "", "", "bp", "", "", ""],
#   ["", "", "", "", "", "", "", ""],
#   ["", "", "", "", "", "", "", ""],
#   ["", "", "", "", "", "", "", ""],
#   ["", "", "", "", "", "", "", ""],
#   ["", "", "wp", "", "", "", "", ""],
#   ["wr", "", "", "wq", "wk", "wb", "", "wr"]
#]


class Button:
    def __init__(self, image, x, y, scale):
        w = image.get_width()
        h = image.get_height()
        self.image = pygame.transform.scale(image, (w*scale / 100, h*scale / 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def get_rect(self):
        return self.rect


def draw_board(surface):
    square_num = 1
    for i in range(0, 8):
        for j in range(0, 8):
            square_num += 1
            if i % 2 == 0:
                if square_num % 2 == 0:
                    color = BLACK_SQUARES_COLOR
                else:
                    color = WHITE_SQUARES_COLOR
            else:
                if square_num % 2 == 0:
                    color = WHITE_SQUARES_COLOR
                else:
                    color = BLACK_SQUARES_COLOR
            pygame.draw.rect(surface, color, pygame.Rect(j * square_length, i * square_length,
                                                         square_length, square_length))


def create_starting_position():
    x, y = 0, 0

    for row in starting_board:
        for piece in row:
            if piece == "":
                x += 1
                continue
            if piece[1] == "p":
                Pawn(piece[0], x, y)
            elif piece[1] == "b":
                Bishop(piece[0], x, y)
            elif piece[1] == "n":
                Knight(piece[0], x, y)
            elif piece[1] == "r":
                Rook(piece[0], x, y)
            elif piece[1] == "q":
                Queen(piece[0], x, y)
            elif piece[1] == "k":
                King(piece[0], x, y)

            x += 1
        y += 1
        x = 0


def get_opposing_turn(turn):
    if turn == "w":
        return "b"
    if turn == "b":
        return "w"
    # lambda turn: "b" if turn == "w" else ("w" if turn == "b" else None)


def is_winning(turn):
    pieces = Piece.get_pieces_list()
    is_check = False
    if len(pieces) == 2:  # only two kings on the board
        return "draw"

    for piece in pieces:
        if piece.get_team() == turn:
            if piece.get_type() == "k":  # king
                is_check = piece.is_in_check(pieces)
            if get_legal_moves(piece):
                return None  # no winner because there is a legal move
    # no legal moves
    if is_check:
        return get_opposing_turn(turn)
    else:
        return "stalemate"


def on_click(piece_clicked, pieces, turn, piece_clicked_location):
    # selection: past click
    # piece: current click
    row = piece_clicked_location[0]
    col = piece_clicked_location[1]

    selected_piece = Piece.get_selection()

    if piece_clicked is not None and selected_piece is None and piece_clicked.get_team() == turn:  # select piece
        piece_clicked.select()

    elif piece_clicked is None and selected_piece is not None:  # move piece (piece is empty and selection is not)
        is_legal, action = is_legal_move(selected_piece, (row, col))
        if is_legal:
            Move(selected_piece, action, (row, col)).move()
            turn = get_opposing_turn(turn)
        selected_piece.deselect()
    elif piece_clicked is not None and selected_piece is not None:  # selection take piece
        if piece_clicked.get_team() == selected_piece.get_team():
            piece_clicked.select()
        else:  # not the same team so can take
            is_legal, action = is_legal_move(selected_piece, (row, col))
            if is_legal:
                Move(selected_piece, action, (row, col)).move()

                turn = get_opposing_turn(turn)

            selected_piece.deselect()

    update_protection(pieces)
    return turn


def check_promotion(pieces):
    for piece in pieces:
        if piece.get_type() == "p" and (piece.get_col() == 7 or piece.get_col() == 0):
            return piece
    return None


def reset_game():
    Piece.reset_pieces_list()
    create_starting_position()


def draw_circle(surface, square, color=GRAY):
    pygame.draw.circle(surface, color,
                       (square[0] * square_length + square_length / 2,  # x
                        square[1] * square_length + square_length / 2),  # y
                       0.25 * square_length)  # radius


def draw_screen(surface, pieces, turn, winner, promotion, promotion_pieces, reset_button):
    surface.fill(BACKGROUND)
    if turn == "w":
        surface.blit(white_turn, (square_length * 8 + 20, 20))
    else:
        surface.blit(black_turn, (square_length * 8 + 20, 20))
    if winner:
        if winner == "w":
            screen.blit(white_won, (square_length * 8 + 20, square_length*8/2 - 60))
            screen.blit(checkmate, (square_length * 8 + 20, square_length*8/2 - 20))
        elif winner == "b":
            screen.blit(black_won, (square_length * 8 + 20, square_length*8/2 - 60))
            screen.blit(checkmate, (square_length * 8 + 20, square_length*8/2 - 20))
        elif winner == "stalemate":
            screen.blit(stalemate, (square_length * 8 + 20, square_length * 8 / 2 - 60))
        elif winner == "draw":
            screen.blit(no_pieces1, (square_length * 8 + 20, square_length * 8 / 2 - 60))
            screen.blit(no_pieces2, (square_length * 8 + 20, square_length * 8 / 2 - 20))
            screen.blit(no_pieces3, (square_length * 8 + 20, square_length * 8 / 2 + 20))
    draw_board(surface)
    for piece in pieces:
        if piece.get_type() == "k" and piece.is_in_check(pieces):
            if piece.get_team() == "w":
                screen.blit(white_check, (square_length * 8 + 20, square_length + 20))
            else:
                screen.blit(black_check, (square_length * 8 + 20, square_length + 20))
        surface.blit(piece.get_image(), piece.get_pos())
    selected_piece = Piece.get_selection()

    if promotion and promotion_pieces:
        surface.blit(promote, (square_length * 8 + 20, square_length * 6 / 4))
        for piece in promotion_pieces:
            surface.blit(piece.get_image(), piece.get_pos())

    if selected_piece:
        moves = get_legal_moves(selected_piece)
        for square in moves:
            draw_circle(surface, square.get_dest())
    reset_button.draw()
    pygame.display.update()


def main():
    # Game loop
    create_starting_position()
    pieces = Piece.get_pieces_list()
    reset_button = Button(reset_image, square_length * 8 + 20, square_length * 7, 50)
    turn = "w"
    winner = None
    promotion = None
    promotion_pieces = None
    pause = False
    running = True
    update_protection(pieces)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = x//square_length, y//square_length
                if reset_button.get_rect().collidepoint((x, y)):
                    reset_game()
                    turn = "w"
                    winner = None
                    pause = False
                    pieces = Piece.get_pieces_list()
                    update_protection(pieces)
                if not pause:
                    piece = get_square_contents(row, col, pieces)
                    turn = on_click(piece, pieces, turn, (row, col))
                    promotion = check_promotion(pieces)
                    if promotion:
                        pause = True
                    winner = is_winning(turn)
                    if winner:
                        pause = True
                        if winner == "w":
                            print("White won!")
                        elif winner == "b":
                            print("Black won!")
                        elif winner == "draw":
                            print("draw")
                if pause and promotion:
                    team = promotion.get_team()
                    piece_x = (square_length * 9) // square_length
                    piece_y = (square_length * 7 / 4) // square_length
                    promotion_pieces = [Queen(team, piece_x, piece_y + 1),
                                        Rook(team, piece_x, piece_y + 2),
                                        Bishop(team, piece_x, piece_y + 3),
                                        Knight(team, piece_x, piece_y + 4)
                                        ]

                    piece = None
                    if x > square_length * 8:
                        piece = get_square_contents(row, col, promotion_pieces)
                    if piece:
                        piece.moveto(promotion.get_row(), promotion.get_col())
                        promotion.remove()
                        promotion = None
                        pause = False
                    for p in promotion_pieces:
                        if p != piece:
                            p.remove()
        if running:
            draw_screen(screen, pieces, turn, winner, promotion, promotion_pieces, reset_button)


if __name__ == "__main__":
    main()
