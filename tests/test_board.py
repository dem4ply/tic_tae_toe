from unittest import TestCase
from unittest.mock import Mock, patch
from board import Board


class Test_menu( TestCase ):
    def test_init( self ):
        window = Mock()
        board = Board( window )

        blank = [ [ ' ', ' ', ' ' ], [ ' ', ' ', ' ' ], [ ' ', ' ', ' ' ] ]

        self.assertListEqual( board.pieces, blank  )
        self.assertIsNone( board.preview_piece )

        return board

    def test_set_piece_x( self ):
        board = self.test_init()
        board.set_x( 0, 0 )
        expected = [ [ board.X, ' ', ' ' ], [ ' ', ' ', ' ' ],
                     [ ' ', ' ', ' ' ] ]

        self.assertListEqual( board.pieces, expected )
        board.set_x( 1, 1 )
        expected[1][1] = board.X
        self.assertListEqual( board.pieces, expected )

    def test_set_piece_o( self ):
        board = self.test_init()
        board.set_o( 0, 0 )
        expected = [ [ board.O, ' ', ' ' ], [ ' ', ' ', ' ' ],
                     [ ' ', ' ', ' ' ] ]

        self.assertListEqual( board.pieces, expected )
        board.set_o( 1, 1 )
        expected[1][1] = board.O
        self.assertListEqual( board.pieces, expected )

    @patch( 'curses.color_pair' )
    def test_draw_piece( self, curs ):
        board = self.test_init()
        board.set_x( 1, 1 )
        board.set_o( 0, 0 )
        board.draw_piece( 0, 0 )
        board.draw_piece( 1, 1 )

    def test_find_empty_space( self ):
        board = self.test_init()
        vector = board.find_empty_space()
        self.assertTupleEqual( vector, ( 0, 0 ) )
        board.set_o( 0, 0 )
        vector = board.find_empty_space()
        self.assertTupleEqual( vector, ( 0, 1 ) )

    def test_evaluate_board( self ):
        board = self.test_init()
        test_board = [['X', 'X', 'O'], ['X', 'X', ' '], ['O', 'O', 'O']]
        result = board.evaluate_board( test_board )
        self.assertEqual( result, 2 )
