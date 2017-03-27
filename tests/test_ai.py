from unittest import TestCase
from unittest.mock import Mock
from ai import AI

ai_tree = {}
p2 = AI( ai_tree, 2 )
p2.build_tree()


class Test_ai( TestCase ):
    def test_case_1( self ):
        board = [ [ 'O', 'X', ' ' ],
                  [ ' ', 'X', ' ' ],
                  [ ' ', ' ', ' ' ], ]
        result, move = p2.search_node( board, 'O' )
        x, y = move
        board[x][y] = 'O'
        self.assertTupleEqual( move, ( 2, 1 ) )

    def test_case_2( self ):
        board = [ [ 'X', 'X', ' ' ],
                  [ ' ', ' ', ' ' ],
                  [ 'O', ' ', ' ' ], ]
        result, move = p2.search_node( board, 'O' )
        x, y = move
        board[x][y] = 'O'
        self.assertTupleEqual( move, ( 0, 2 ) )
