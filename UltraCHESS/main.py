import pygame


class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.s_width = width // 8
		self.s_height = height // 8
		self.on_piece = None
		self.turn = 'white'

		self.board_layout = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'b '],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'w '],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
		]
		self.squares = self.makeSquares()
		self.initBoard()

	def makeSquares(self):
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(
						x,
						y,
						self.s_width,
						self.s_height
					)
				)

		return output


	def initBoard(self):
		for y, row in enumerate(self.board_layout):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.getSquarePosition((x, y))

					if piece[1] == 'R':
						square.on_piece = Rook(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'N':
						square.on_piece = Knight(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'B':
						square.on_piece = Bishop(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'Q':
						square.on_piece = Queen(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == 'K':
						square.on_piece = King(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)

					elif piece[1] == ' ':
						square.on_piece = Pawn(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self
						)


	def onClick(self, mx, my):
		x = mx // self.s_width
		y = my // self.s_height
		clicked_square = self.getSquarePosition((x, y))

		if self.on_piece is None:
			if clicked_square.on_piece is not None:
				if clicked_square.on_piece.color == self.turn:
					self.on_piece = clicked_square.on_piece

		elif self.on_piece.move(self, clicked_square):
			self.turn = 'white' if self.turn == 'black' else 'black'

		elif clicked_square.on_piece is not None:
			if clicked_square.on_piece.color == self.turn:
				self.on_piece = clicked_square.on_piece


	def inCheck(self, color, board_change=None):
		output = False
		king_pos = None

		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.on_piece
					old_square = square
					old_square.on_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.on_piece
					new_square.on_piece = changing_piece

		pieces = [
			i.on_piece for i in self.squares if i.on_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K':
					if piece.color == color:
						king_pos = piece.pos
		for piece in pieces:
			if piece.color != color:
				for square in piece.returnMovesHint(self):
					if square.pos == king_pos:
						output = True

		if board_change is not None:
			old_square.on_piece = changing_piece
			new_square.on_piece = new_square_old_piece
						
		return output


	def inCheckmate(self, color):
		output = False

		for piece in [i.on_piece for i in self.squares]:
			if piece != None:
				if piece.notation == 'K' and piece.color == color:
					king = piece

		if king.getValidMovesHint(self) == []:
			if self.inCheck(color):
				output = True

		return output


	def getSquarePosition(self, pos):
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square


	def getPieceOnPosition(self, pos):
		return self.getSquarePosition(pos).on_piece


	def draw(self, display):
		if self.on_piece is not None:
			self.getSquarePosition(self.on_piece.pos).highlight = True
			for square in self.on_piece.getValidMovesHint(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)


class Piece:
	def __init__(self, pos, color, board):
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		self.color = color
		self.has_moved = False

	def move(self, board, square, force=False):

		for i in board.squares:
			i.highlight = False

		if square in self.getValidMovesHint(board) or force:
			prev_square = board.getSquarePosition(self.pos)
			self.pos, self.x, self.y = square.pos, square.x, square.y

			prev_square.on_piece = None
			square.on_piece = self
			board.selected_piece = None
			self.has_moved = True

			# Pawn promotion
			if self.notation == ' ':
				if self.y == 0 or self.y == 7:
					square.on_piece = Queen(
						(self.x, self.y),
						self.color,
						board
					)

			# Move rook if king castles
			if self.notation == 'K':
				if prev_square.x - self.x == 2:
					rook = board.getPieceOnPosition((0, self.y))
					rook.move(board, board.getSquarePosition((3, self.y)), force=True)
				elif prev_square.x - self.x == -2:
					rook = board.getPieceOnPosition((7, self.y))
					rook.move(board, board.getSquarePosition((5, self.y)), force=True)

			return True
		else:
			board.selected_piece = None
			return False


	def getAllMoves(self, board):
		output = []
		for direction in self.getPossibleMovesHint(board):
			for square in direction:
				if square.on_piece is not None:
					if square.on_piece.color == self.color:
						break
					else:
						output.append(square)
						break
				else:
					output.append(square)

		return output


	def getValidMovesHint(self, board):
		output = []
		for square in self.getAllMoves(board):
			if not board.inCheck(self.color, board_change=[self.pos, square.pos]):
				output.append(square)

		return output


	# True for all pieces except pawn
	def returnMovesHint(self, board):
		return self.getAllMoves(board)
	
	
class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.highlighter = (255, 51, 51) if self.color == 'light' else (204, 0, 0)
        self.on_piece = None
        self.coord = self.getCoordinates()
        self.highlight = False

        self.rect = pygame.Rect(
            self.abs_x,
            self.abs_y,
            self.width,
            self.height
        )

    def getCoordinates(self):
        columns = 'abcdefgh'
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        # Load the textures
        ground_texture = pygame.image.load('res/images/ground.png')
        grass_texture = pygame.image.load('res/images/grass.png')

        # Set the texture based on the cell color
        cell_texture = ground_texture if self.color == 'dark' else grass_texture

        # Draw the cell with the selected texture
        if self.highlight:
            pygame.draw.rect(display, self.highlighter, self.rect)
        else:
            display.blit(cell_texture, self.rect)

        if self.on_piece is not None:
            centering_rect = self.on_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.on_piece.img, centering_rect.topleft)


class Queen(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		path_to_image = 'res/images/' + color[0] + '_queen.png'
		self.img = pygame.image.load(path_to_image)
		self.img = pygame.transform.scale(self.img, (board.s_width - 20, board.s_height - 20))

		self.notation = 'Q'


	def getPossibleMovesHint(self, board):
		output = []

		moves_north = []
		for y in range(self.y)[::-1]:
			moves_north.append(board.getSquarePosition(
				(self.x, y)
			))
		output.append(moves_north)

		moves_ne = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y - i < 0:
				break
			moves_ne.append(board.getSquarePosition(
				(self.x + i, self.y - i)
			))
		output.append(moves_ne)

		moves_east = []
		for x in range(self.x + 1, 8):
			moves_east.append(board.getSquarePosition(
				(x, self.y)
			))
		output.append(moves_east)

		moves_se = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y + i > 7:
				break
			moves_se.append(board.getSquarePosition(
				(self.x + i, self.y + i)
			))
		output.append(moves_se)

		moves_south = []
		for y in range(self.y + 1, 8):
			moves_south.append(board.getSquarePosition(
				(self.x, y)
			))
		output.append(moves_south)

		moves_sw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y + i > 7:
				break
			moves_sw.append(board.getSquarePosition(
				(self.x - i, self.y + i)
			))
		output.append(moves_sw)

		moves_west = []
		for x in range(self.x)[::-1]:
			moves_west.append(board.getSquarePosition(
				(x, self.y)
			))
		output.append(moves_west)

		moves_nw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y - i < 0:
				break
			moves_nw.append(board.getSquarePosition(
				(self.x - i, self.y - i)
			))
		output.append(moves_nw)

		return output


class Rook(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		path_to_image = 'res/images/' + color[0] + '_rook.png'
		self.img = pygame.image.load(path_to_image)
		self.img = pygame.transform.scale(self.img, (board.s_width - 20, board.s_height - 20))

		self.notation = 'R'


	def getPossibleMovesHint(self, board):
		output = []

		moves_north = []
		for y in range(self.y)[::-1]:
			moves_north.append(board.getSquarePosition(
				(self.x, y)
			))
		output.append(moves_north)

		moves_east = []
		for x in range(self.x + 1, 8):
			moves_east.append(board.getSquarePosition(
				(x, self.y)
			))
		output.append(moves_east)

		moves_south = []
		for y in range(self.y + 1, 8):
			moves_south.append(board.getSquarePosition(
				(self.x, y)
			))
		output.append(moves_south)

		moves_west = []
		for x in range(self.x)[::-1]:
			moves_west.append(board.getSquarePosition(
				(x, self.y)
			))
		output.append(moves_west)

		return output
	

class Pawn(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		path_to_image = 'res/images/' + color[0] + '_pawn.png'
		self.img = pygame.image.load(path_to_image)
		self.img = pygame.transform.scale(self.img, (board.s_width - 35, board.s_height - 35))
		self.notation = ' '


	def getPossibleMovesHint(self, board):
		output = []
		moves = []

		# move forward
		if self.color == 'white':
			moves.append((0, -1))
			if not self.has_moved:
				moves.append((0, -2))

		elif self.color == 'black':
			moves.append((0, 1))
			if not self.has_moved:
				moves.append((0, 2))

		for move in moves:
			new_pos = (self.x, self.y + move[1])
			if new_pos[1] < 8 and new_pos[1] >= 0:
				output.append(
					board.getSquarePosition(new_pos)
				)

		return output


	def getAllMoves(self, board):
		output = []
		for square in self.getPossibleMovesHint(board):
			if square.on_piece != None:
				break
			else:
				output.append(square)

		if self.color == 'white':
			if self.x + 1 < 8 and self.y - 1 >= 0:
				square = board.getSquarePosition(
					(self.x + 1, self.y - 1)
				)
				if square.on_piece != None:
					if square.on_piece.color != self.color:
						output.append(square)
			if self.x - 1 >= 0 and self.y - 1 >= 0:
				square = board.getSquarePosition(
					(self.x - 1, self.y - 1)
				)
				if square.on_piece != None:
					if square.on_piece.color != self.color:
						output.append(square)

		elif self.color == 'black':
			if self.x + 1 < 8 and self.y + 1 < 8:
				square = board.getSquarePosition(
					(self.x + 1, self.y + 1)
				)
				if square.on_piece != None:
					if square.on_piece.color != self.color:
						output.append(square)
			if self.x - 1 >= 0 and self.y + 1 < 8:
				square = board.getSquarePosition(
					(self.x - 1, self.y + 1)
				)
				if square.on_piece != None:
					if square.on_piece.color != self.color:
						output.append(square)

		return output

	def returnMovesHint(self, board):
		moves = self.getAllMoves(board)
		# return the diagonal moves 
		return [i for i in moves if i.x != self.x]


class Knight(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		path_to_image = 'res/images/' + color[0] + '_knight.png'
		self.img = pygame.image.load(path_to_image)
		self.img = pygame.transform.scale(self.img, (board.s_width - 20, board.s_height - 20))

		self.notation = 'N'


	def getPossibleMovesHint(self, board):
		out = []
		moves = [(1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2)]

		for move in moves:
			new_position = (self.x + move[0], self.y + move[1])
			if (new_position[0] < 8 and new_position[0] >= 0 and new_position[1] < 8 and new_position[1] >= 0):
				out.append([board.getSquarePosition(new_position)])

		return out
	

class King(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		path_to_image = 'res/images/' + color[0] + '_king.png'
		self.img = pygame.image.load(path_to_image)
		self.img = pygame.transform.scale(self.img, (board.s_width - 20, board.s_height - 20))

		self.notation = 'K'


	def getPossibleMovesHint(self, board):
		output = []
		moves = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

		for move in moves:
			new_pos = (self.x + move[0], self.y + move[1])
			if (new_pos[0] < 8 and new_pos[0] >= 0 and new_pos[1] < 8 and new_pos[1] >= 0):
				output.append([board.getSquarePosition(new_pos)])

		return output

	def canDoCastle(self, board):
		if not self.has_moved:

			if self.color == 'white':
				queenside_rook = board.getPieceOnPosition((0, 7))
				kingside_rook = board.getPieceOnPosition((7, 7))
				if queenside_rook != None:
					if not queenside_rook.has_moved:
						if [
							board.getPieceOnPosition((i, 7)) for i in range(1, 4)
						] == [None, None, None]:
							return 'queenside'
				if kingside_rook != None:
					if not kingside_rook.has_moved:
						if [
							board.getPieceOnPosition((i, 7)) for i in range(5, 7)
						] == [None, None]:
							return 'kingside'

			elif self.color == 'black':
				queenside_rook = board.getPieceOnPosition((0, 0))
				kingside_rook = board.getPieceOnPosition((7, 0))
				if queenside_rook != None:
					if not queenside_rook.has_moved:
						if [
							board.getPieceOnPosition((i, 0)) for i in range(1, 4)
						] == [None, None, None]:
							return 'queenside'
				if kingside_rook != None:
					if not kingside_rook.has_moved:
						if [board.getPieceOnPosition((i, 0)) for i in range(5, 7)] == [None, None]:
							return 'kingside'


	def getValidMovesHint(self, board):
		output = []
		for square in self.getAllMoves(board):
			if not board.inCheck(self.color, board_change=[self.pos, square.pos]):
				output.append(square)

		if self.canDoCastle(board) == 'queenside':
			output.append(
				board.getSquarePosition((self.x - 2, self.y))
			)
		if self.canDoCastle(board) == 'kingside':
			output.append(
				board.getSquarePosition((self.x + 2, self.y))
			)

		return output


class Bishop(Piece):
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		img_path = 'res/images/' + color[0] + '_bishop.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.s_width - 20, board.s_height - 20))

		self.notation = 'B'


	def getPossibleMovesHint(self, board):
		output = []

		moves_ne = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y - i < 0:
				break
			moves_ne.append(board.getSquarePosition(
				(self.x + i, self.y - i)
			))
		output.append(moves_ne)

		moves_se = []
		for i in range(1, 8):
			if self.x + i > 7 or self.y + i > 7:
				break
			moves_se.append(board.getSquarePosition(
				(self.x + i, self.y + i)
			))
		output.append(moves_se)

		moves_sw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y + i > 7:
				break
			moves_sw.append(board.getSquarePosition(
				(self.x - i, self.y + i)
			))
		output.append(moves_sw)

		moves_nw = []
		for i in range(1, 8):
			if self.x - i < 0 or self.y - i < 0:
				break
			moves_nw.append(board.getSquarePosition(
				(self.x - i, self.y - i)
			))
		output.append(moves_nw)

		return output


pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()

running = True
while running:
	mx, my = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				board.onClick(mx, my)

	if board.inCheckmate('black'):
		print('')
		running = False
	elif board.inCheckmate('white'):
		print('Black wins!')
		running = False
	draw(screen)