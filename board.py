import curses


class Board:
    X = 'X'
    O = 'O'
    BLANK = ' '

    def __init__( self, windows ):
        self.windows = windows
        self.pieces = []
        self.clean_pieces()

        self.preview_piece = None
        self.status = -1

    def clean_pieces( self ):
        self.pieces = [ [ self.BLANK for _ in range( 3 ) ] for _ in range( 3 ) ]
        self.status = -1

    def set_piece( self, piece, x, y ):
        self.pieces[ x ][ y ] = piece
        self.evaluate_board()

    def set_x( self, x, y ):
        self.set_piece( self.X, x, y )

    def set_o( self, x, y ):
        self.set_piece( self.O, x, y )

    def set_blank( self, x, y ):
        self.set_piece( self.BLANK, x, y )

    def draw( self ):
        row = '+---+---+---+'
        init_bar = '|'
        end_bar = '  ' + init_bar[::-1]

        self.windows.clear()

        for i in range( 3 ):
            self.windows.addstr( row )
            self.windows.addstr( init_bar )
            for j in range( 3 ):
                self.draw_piece( i, j )
                self.windows.addstr( end_bar )
        self.windows.addstr( row )
        self.windows.refresh()
        '''
        +---+---+---+
        | O | O | X |
        +---+---+---+
        | X | X | O |
        +---+---+---+
        | O | O | X |
        +---+---+---+
        '''

    def draw_piece( self, x, y ):
        if self.preview_piece is not None:
            p_piece, p_x, p_y, = self.preview_piece
            if x == p_x and y == p_y:
                self.windows.addstr( p_piece, curses.color_pair(3) )
                return
        piece = self.pieces[x][y]
        if piece == self.X:
            self.windows.addstr( piece, curses.color_pair(1) )
        else:
            self.windows.addstr( piece, curses.color_pair(2) )

    def set_preview( self, piece ):
        vector = self.find_empty_space()
        if vector is None:
            self.preview_piece = None
            return False

        x, y = vector
        self.preview_piece = ( piece, x, y )
        return True

    def find_empty_space( self, matrix=None ):
        if matrix == None:
            matrix = self.pieces
        for i in range( 3 ):
            for j in range( 3 ):
                if matrix[i][j] == self.BLANK:
                    return i, j

    @property
    def is_end_game( self ):
        return self.status != -1

    def evaluate_board( self, matrix=None ):
        if matrix is None:
            matrix = self.pieces
        for row in matrix:
            is_win = self.eval_row( row, self.X )
            if is_win:
                self.status = 1
                return 1
            is_win = self.eval_row( row, self.O )
            if is_win:
                self.status = 2
                return 2
        inver = zip( *matrix )
        for row in inver:
            is_win = self.eval_row( row, self.X )
            if is_win:
                self.status = 1
                return 1
            is_win = self.eval_row( row, self.O )
            if is_win:
                self.status = 2
                return 2
        row = [ matrix[0][0], matrix[1][1], matrix[2][2], ]
        is_win = self.eval_row( row, self.X )
        if is_win:
            self.status = 1
            return 1
        is_win = self.eval_row( row, self.O )
        if is_win:
            self.status = 2
            return 2

        row = [ matrix[0][2], matrix[1][1], matrix[2][0], ]
        is_win = self.eval_row( row, self.X )
        if is_win:
            self.status = 1
            return 1
        is_win = self.eval_row( row, self.O )
        if is_win:
            self.status = 2
            return 2
        have_blank = self.find_empty_space( matrix )
        if have_blank is None:
            self.status = 0
            return 0

    def eval_row( self, row, piece ):
        count = 0
        for j in range( 3 ):
            if row[j] == piece:
                count += 1
            else:
                break
        if count == 3:
            return True
        return False


    def choice_preview( self ):
        p_piece, p_x, p_y, = self.preview_piece
        self.set_piece( p_piece, p_x, p_y )

    def up_preview( self ):
        p_piece, p_x, p_y, = self.preview_piece
        origin_x, origin_y = ( p_x, p_y )
        for x in range( 3 ):
            for y in range ( 3 ):
                p_y += 1
                if p_y > 2:
                    p_y = 0
                if self.pieces[ p_x ][ p_y ] == self.BLANK:
                    self.preview_piece = ( p_piece, p_x, p_y )
            p_x += 1
            if p_x > 2:
                p_x = 0

    def down_preview( self ):
        p_piece, p_x, p_y, = self.preview_piece
        origin_x, origin_y = ( p_x, p_y )
        for x in range( 3 ):
            for y in range ( 3 ):
                p_y -= 1
                if p_y < 0:
                    p_y = 2
                if self.pieces[ p_x ][ p_y ] == self.BLANK:
                    self.preview_piece = ( p_piece, p_x, p_y )
            p_x -= 1
            if p_x < 0:
                p_x = 2

    def right_preview( self ):
        p_piece, p_x, p_y, = self.preview_piece
        origin_x, origin_y = ( p_x, p_y )
        for x in range( 3 ):
            for y in range ( 3 ):
                p_x -= 1
                if p_x < 0:
                    p_x = 2
                if self.pieces[ p_x ][ p_y ] == self.BLANK:
                    self.preview_piece = ( p_piece, p_x, p_y )
            p_y -= 1
            if p_y < 0:
                p_y = 2

    def left_preview( self ):
        p_piece, p_x, p_y, = self.preview_piece
        origin_x, origin_y = ( p_x, p_y )
        for x in range( 3 ):
            for y in range ( 3 ):
                p_x += 1
                if p_x > 2:
                    p_x = 0
                if self.pieces[ p_x ][ p_y ] == self.BLANK:
                    self.preview_piece = ( p_piece, p_x, p_y )
            p_y += 1
            if p_y > 2:
                p_y = 0
