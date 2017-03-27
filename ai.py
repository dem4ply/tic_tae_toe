import copy
from board import Board
from unittest.mock import Mock
import random


class Node:
    def __init__( self, value, who_win, move, current_piece ):
        self.value = value
        self.who_win = who_win
        self.move = move
        self.children = []
        self.piece = current_piece

    def add_child( self, node ):
        self.children.append( node )

    def __repr__( self ):
        return '<{}({}, {}, {})>'.format( self.__class__, self.who_win,
                                          self.move, self.piece )

class AI:
    def __init__( self, ai_tree, player ):
        self.tree = ai_tree
        self.player = player

    def build_tree( self ):
        board = Board( Mock() )
        matrix = copy.deepcopy( board.pieces )
        who_win = board.evaluate_board( matrix )
        move = None
        node = Node( matrix, who_win, move, ' ' )
        self.tree[ str(matrix) ] = node
        self.build_subtree( node, matrix, board.X, board )

    def build_subtree( self, parent, matrix, current_piece, board ):
        blanks = self.get_blanks( matrix )
        for x, y in blanks:
            new_matrix = copy.deepcopy( matrix )
            new_matrix[x][y] = current_piece
            try:
                node = self.tree[ str( new_matrix ) ]
                parent.add_child( node )
            except KeyError:
                who_win = board.evaluate_board( new_matrix )
                node = Node( new_matrix, who_win, ( x, y ), current_piece )
                self.tree[ str( new_matrix ) ] = node
                parent.add_child( node )
                if who_win == None:
                    self.build_subtree(
                        node, new_matrix,
                        Board.O if current_piece==Board.X else Board.X,
                        board )

    def get_blanks( self, matrix ):
        result = []
        for i, row in enumerate( matrix ):
            for j, cell in enumerate( row ):
                if cell == Board.BLANK:
                    result.append( ( i, j ) )
        return result

    def do_you_thing( self, board ):
        self.current_board = board.pieces
        self.temp_board = Board( Mock() )
        current_piece = Board.O if self.player==2 else Board.X
        is_empty = True
        for row in board.pieces:
            for piece in row:
                if piece != ' ':
                    is_empty = False
                    break
        if is_empty:
            move = ( random.randint( 0, 2 ), random.randint( 0, 2 ) )
        else:
            score, move = self.search_node( self.current_board, current_piece )
        x, y = move
        if self.player == 1:
            board.set_x( x, y )
        else:
            board.set_o( x, y )


    def search_node( self, board, current_piece, depth=0 ):
        if self.player == 2:
            is_player = current_piece == Board.O
        else:
            is_player = current_piece == Board.X
        try:
            who_win = self.temp_board.evaluate_board( board )
        except AttributeError:
            self.temp_board = Board( Mock() )
            who_win = self.temp_board.evaluate_board( board )
        if who_win is None:
            blanks = self.get_blanks( board )
            best_score = -2
            move = None
            for x, y in blanks:
                new_board = copy.deepcopy( board )
                new_board[x][y] = current_piece
                try:
                    this_score, new_move = self.tree[ str( new_board ) ]
                except KeyError:
                    this_score, new_move = self.search_node(
                        new_board,
                        Board.O if current_piece==Board.X else Board.X, depth=depth+1 )
                    self.tree[ str( new_board ) ] = ( this_score, new_board )
                if -this_score > best_score:
                    move = ( x, y )
                    best_score = -this_score
        elif who_win == self.player:
            if is_player:
                return 1, None
            else:
                return -1, None
        elif who_win == 0:
            return 0, None
        else:
            if is_player:
                return -1, None
            else:
                return 1, None
        return best_score, move
