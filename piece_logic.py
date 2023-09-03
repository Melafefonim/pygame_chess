import pygame

square_length = 80
piece_scale = 80


piece_to_picture = {  # black pieces
    "bb": pygame.image.load("piece_textures/bb.png"),
    "bk": pygame.image.load("piece_textures/bk.png"),
    "bn": pygame.image.load("piece_textures/bn.png"),
    "bp": pygame.image.load("piece_textures/bp.png"),
    "bq": pygame.image.load("piece_textures/bq.png"),
    "br": pygame.image.load("piece_textures/br.png"),
    # white pieces
    "wb": pygame.image.load("piece_textures/wb.png"),
    "wk": pygame.image.load("piece_textures/wk.png"),
    "wn": pygame.image.load("piece_textures/wn.png"),
    "wp": pygame.image.load("piece_textures/wp.png"),
    "wq": pygame.image.load("piece_textures/wq.png"),
    "wr": pygame.image.load("piece_textures/wr.png")
}


class Piece:

    pieces_list = []
    selection = None

    def __init__(self, team, type, row, col, size=piece_scale):
        Piece.pieces_list.append(self)
        self.team = team
        self.type = type
        self.row = row
        self.col = col
        self.image = pygame.transform.scale(piece_to_picture[team + type], (size, size))
        self.pos = square_length / 2 - self.image.get_width() / 2 + row * square_length, \
                   square_length / 2 - self.image.get_height() / 2 + col * square_length
        self.moved = False
        self.protected = False

    @classmethod
    def get_pieces_list(cls):
        return cls.pieces_list

    @classmethod
    def reset_pieces_list(cls):
        cls.pieces_list = []

    def get_team(self):
        return self.team

    def get_type(self):
        return self.type

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_image(self):
        return self.image

    def get_square(self):
        return self.row, self.col

    def get_pos(self):
        return self.pos

    def moveto(self, row, col):
        self.row = row
        self.col = col
        self.pos = square_length / 2 - self.image.get_width() / 2 + row * square_length, \
                   square_length / 2 - self.image.get_height() / 2 + col * square_length
        self.moved = True

    def take(self, piece):
        self.moveto(*piece.get_square())
        piece.remove()

    @staticmethod
    def deselect():
        Piece.selection = None

    @staticmethod
    def get_selection():
        return Piece.selection

    def select(self):
        Piece.selection = self

    def protect(self):
        self.protected = True

    def unprotect(self):
        self.protected = False

    def is_protected(self):
        return self.protected

    def remove(self):
        Piece.get_pieces_list().remove(self)

    def get_king(self):
        for piece in Piece.get_pieces_list():
            if piece.get_team() == self.get_team() and piece.get_type() == "k":
                return piece


class Pawn(Piece):
    def __init__(self, team, row, col, size=piece_scale):
        Piece.__init__(self, team, "p", row, col, size)

    def get_possible_moves(self):
        x = self.get_row()
        y = self.get_col()
        pieces_list = Piece.get_pieces_list()

        takes = []
        possible_moves = []

        if self.get_team() == "w":
            if x > 0:
                takes.append(Move(self, "take", (x - 1, y - 1)))
            if x < 7:
                takes.append(Move(self, "take", (x + 1, y - 1)))
            moves = [Move(self, "move", (x, y - 1))]
            if not self.moved:
                moves.append(Move(self, "move", (x, y - 2)))
        else:
            if x > 0:
                takes.append(Move(self, "take", (x - 1, y + 1)))
            if x < 7:
                takes.append(Move(self, "take", (x + 1, y + 1)))
            moves = [Move(self, "move", (x, y + 1))]
            if not self.moved:
                moves.append(Move(self, "move", (x, y + 2)))
        for take in takes:
            square_content = get_square_contents(*take.get_dest(), pieces_list)
            if square_content is not None and square_content.get_team() != self.get_team():
                possible_moves.append(take)
            elif square_content is not None:
                square_content.protect()
        for move in moves:
            if get_square_contents(*move.get_dest(), pieces_list) is None:
                possible_moves.append(move)
            else:
                break
        return possible_moves

    def get_controlling_squares(self):
        x = self.get_row()
        y = self.get_col()

        takes = []

        if self.get_team() == "w":
            if x > 0:
                takes.append(Move(self, "take", (x - 1, y - 1)))
            if x < 7:
                takes.append(Move(self, "take", (x + 1, y - 1)))
        else:
            if x > 0:
                takes.append(Move(self, "take", (x - 1, y + 1)))
            if x < 7:
                takes.append(Move(self, "take", (x + 1, y + 1)))

        return takes


class Bishop(Piece):
    def __init__(self, team, row, col, size=piece_scale):
        Piece.__init__(self, team, "b", row, col, size)

    def get_possible_moves(self):
        pieces_list = Piece.get_pieces_list()
        x = self.get_row()
        y = self.get_col()
        moves = []
        for i in range(1, 8):  # top left diagonal
            if x - i < 0 or y - i < 0:
                break
            square_content = get_square_contents(x - i, y - i, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x - i, y - i)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x - i, y - i)))
                break
            else:
                square_content.protect()
                break

        for i in range(1, 8):  # top right diagonal
            if x + i > 7 or y - i < 0:
                break
            square_content = get_square_contents(x + i, y - i, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x + i, y - i)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x + i, y - i)))
                break
            else:
                square_content.protect()
                break

        for i in range(1, 8):  # bottom left diagonal
            if x - i < 0 or y + i > 7:
                break
            square_content = get_square_contents(x - i, y + i, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x - i, y + i)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x - i, y + i)))
                break
            else:
                square_content.protect()
                break

        for i in range(1, 8):  # bottom right diagonal
            if x + i > 7 or y + i > 7:
                break
            square_content = get_square_contents(x + i, y + i, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x + i, y + i)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x + i, y + i)))
                break
            else:
                square_content.protect()
                break
        return moves


class Knight(Piece):
    def __init__(self, team, row, col, size=piece_scale):
        Piece.__init__(self, team, "n", row, col, size)

    def get_possible_moves(self):
        pieces_list = Piece.get_pieces_list()
        x = self.get_row()
        y = self.get_col()
        moves = [(x - 1, y - 2), (x + 1, y - 2),
                 (x + 2, y - 1), (x + 2, y + 1),
                 (x - 1, y + 2), (x + 1, y + 2),
                 (x - 2, y - 1), (x - 2, y + 1)
                 ]
        possible_moves = []
        for move in moves:

            if not (move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7):
                square_content = get_square_contents(*move, pieces_list)
                if square_content is not None and square_content.get_team() != self.get_team():
                    possible_moves.append(Move(self, "take", move))
                else:
                    if square_content is None:
                        possible_moves.append(Move(self, "move", move))
                    else:
                        square_content.protect()
        return possible_moves


class King(Piece):
    def __init__(self, team, row, col, size=piece_scale):
        Piece.__init__(self, team, "k", row, col, size)
        self.killable = False

    def get_possible_moves(self):
        pieces_list = Piece.get_pieces_list()
        pieces_list.remove(self)
        x = self.get_row()
        y = self.get_col()
        if self.get_team() == "w":
            enemy_squares = get_controlled_squares("b", pieces_list)
        else:
            enemy_squares = get_controlled_squares("w", pieces_list)
        pieces_list.append(self)
        moves = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                 (x - 1, y), (x + 1, y),
                 (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                 ]
        possible_moves = []
        for move in moves:
            if not (move[0] < 0 or move[1] < 0 or move[0] > 7 or move[1] > 7):
                square_content = get_square_contents(*move, pieces_list)
                if square_content is not None and square_content.get_team() != self.get_team() and not square_content.is_protected():
                    possible_moves.append(Move(self, "take", move))
                elif square_content is None and move not in enemy_squares:
                    possible_moves.append(Move(self, "move", move))
                elif square_content is not None and square_content.get_team() == self.get_team():  # and move not in enemy_squares:
                    square_content.protect()
        if not self.is_moved() and not self.is_in_check(pieces_list):
            if self.get_team() == "w":  # white king
                rook = get_square_contents(7, 7, pieces_list)
                if rook and rook.get_type() == "r" and not rook.is_moved():
                    if get_square_contents(6, 7, pieces_list) is None and get_square_contents(5, 7, pieces_list) is None and \
                            (6, 7) not in enemy_squares and (5, 7) not in enemy_squares:
                        possible_moves.append(Move(self, "castle", (6, 7)))  # castle king side
                rook = get_square_contents(0, 7, pieces_list)
                if rook and rook.get_type() == "r" and not rook.is_moved():
                    if get_square_contents(1, 7, pieces_list) is None and get_square_contents(2, 7, pieces_list) is None and \
                            get_square_contents(3, 7, pieces_list) is None and (1, 7) not in enemy_squares and \
                            (2, 7) not in enemy_squares and (3, 7) not in enemy_squares:
                        possible_moves.append(Move(self, "castle", (2, 7)))  # castle queen side
            else:  # black king
                rook = get_square_contents(7, 0, pieces_list)
                if rook and rook.get_type() == "r" and not rook.is_moved():
                    if get_square_contents(6, 0, pieces_list) is None and get_square_contents(5, 0, pieces_list) is None and \
                            (6, 0) not in enemy_squares and (5, 0) not in enemy_squares:
                        possible_moves.append(Move(self, "castle", (6, 0)))  # castle king
                rook = get_square_contents(0, 0, pieces_list)
                if rook and rook.get_type() == "r" and not rook.is_moved():
                    if get_square_contents(1, 0, pieces_list) is None and get_square_contents(2, 0, pieces_list) is None and \
                            get_square_contents(3, 0, pieces_list) is None and (1, 0) not in enemy_squares and \
                            (2, 0) not in enemy_squares and (3, 0) not in enemy_squares:
                        possible_moves.append(Move(self, "castle", (2, 0)))  # castle queen
        return possible_moves

    def get_controlling_squares(self):
        x = self.get_row()
        y = self.get_col()
        moves = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                 (x - 1, y), (x + 1, y),
                 (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                 ]
        move_objects = []
        for move in moves:
            move_objects.append(Move(self, "move", move))
        return move_objects

    def is_in_check(self, pieces):
        if self.get_team() == "b":
            enemy_moves = get_controlled_squares("w", pieces)
        else:
            enemy_moves = get_controlled_squares("b", pieces)
        if self.get_square() in enemy_moves:
            return True
        return False

    def is_moved(self):
        return self.moved


class Queen(Piece):
    def __init__(self, team, row, col, size=piece_scale):
        Piece.__init__(self, team, "q", row, col, size)

    def get_possible_moves(self):
        bishop = Bishop(self.get_team(), self.get_row(), self.get_col())
        bishop.remove()
        # this bishop isn't supposed to be involve him in the game
        moves = bishop.get_possible_moves()

        rook = Rook(self.get_team(), self.get_row(), self.get_col())
        rook.remove()
        # same with the rook...
        moves.extend(rook.get_possible_moves())

        return moves


class Rook(Piece):
    def __init__(self, team, row, col, size=piece_scale):
        Piece.__init__(self, team, "r", row, col, size)

    def get_possible_moves(self):
        pieces_list = Piece.get_pieces_list()
        x = self.get_row()
        y = self.get_col()
        moves = []
        
        for i in range(1, 8):  # left to right
            if x - i < 0:
                break
            square_content = get_square_contents(x - i, y, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x - i, y)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x - i, y)))
                break
            else:
                square_content.protect()
                break

        for i in range(1, 8):  # right to left
            if x + i > 7:
                break
            square_content = get_square_contents(x + i, y, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x + i, y)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x + i, y)))
                break
            else:
                square_content.protect()
                break

        for i in range(1, 8):  # down to up
            if y > 7:
                break
            square_content = get_square_contents(x, y + i, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x, y + i)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x, y + i)))
                break
            else:
                square_content.protect()
                break

        for i in range(1, 8):  # up to down
            if y > 7:
                break
            square_content = get_square_contents(x, y - i, pieces_list)
            if square_content is None:
                moves.append(Move(self, "move", (x, y - i)))
            elif square_content.get_team() != self.get_team():
                moves.append(Move(self, "take", (x, y - i)))
                break
            else:
                square_content.protect()
                break
        return moves

    def is_moved(self):
        return self.moved


class Move:
    def __init__(self, piece, action, destination):
        self.piece = piece
        self.action = action
        self.x = destination[0]
        self.y = destination[1]

    def get_action(self):
        return self.action

    def get_piece(self):
        return self.piece

    def get_dest(self):
        return self.x, self.y

    def move(self):
        if self.get_action() == "move":
            self.get_piece().moveto(*self.get_dest())
        elif self.get_action() == "take":
            self.get_piece().take(get_square_contents(*self.get_dest(), Piece.get_pieces_list()))
        elif self.get_action() == "castle":
            self.get_piece().moveto(*self.get_dest())
            if self.get_dest() == (6, 7):
                get_square_contents(7, 7, Piece.get_pieces_list()).moveto(5, 7)
            elif self.get_dest() == (2, 7):
                get_square_contents(0, 7, Piece.get_pieces_list()).moveto(3, 7)
            elif self.get_dest() == (6, 0):
                get_square_contents(7, 0, Piece.get_pieces_list()).moveto(5, 0)
            elif self.get_dest() == (2, 0):
                get_square_contents(0, 0, Piece.get_pieces_list()).moveto(3, 0)


def get_square_contents(row, col, pieces):
    for piece in pieces:
        if piece.get_square() == (row, col):
            return piece
    return None


def get_controlled_squares(team, pieces):
    moves = []
    for piece in pieces:
        if piece.get_team() == team:
            if piece.get_type() == "k" or piece.get_type() == "p":
                piece_moves = piece.get_controlling_squares()
            else:
                piece_moves = piece.get_possible_moves()
            for move in piece_moves:
                moves.append(move.get_dest())
    return moves


def get_legal_moves(piece):
    legal_moves = []
    piece_list = Piece.get_pieces_list()
    possible_moves = piece.get_possible_moves()
    x, y = piece.get_row(), piece.get_col()
    attacker = None
    moved = piece.moved

    if piece.get_type() == "k":
        return possible_moves
    for move in possible_moves:
        if move.get_action() == "castle":
            legal_moves.append(move)
            continue
        if piece.get_type() == "q":
            action, dest = move.get_action(), move.get_dest()
            move = Move(piece, action, dest)
        if move.get_action() == "take":
            attacker = get_square_contents(*move.get_dest(), piece_list)  # save taken piece
        move.move()
        if not piece.get_king().is_in_check(piece_list):
            legal_moves.append(move)
        if attacker:
            piece_list.append(attacker)
            attacker = None
    piece.moveto(x, y)
    piece.moved = moved
    return legal_moves


def is_legal_move(piece, destination):
    for move in get_legal_moves(piece):
        if move.get_dest() == destination:
            return True, move.get_action()
    return False, None


def update_protection(pieces):
    for piece in pieces:
        piece.unprotect()
    for piece in pieces:
        piece.get_possible_moves()
