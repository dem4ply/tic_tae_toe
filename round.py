class Round:

    def __init__( self, p1, p2, board ):
        self.p1 = p1
        self.p2 = p2
        self.board = board


    def start( self ):
        while not self.board.is_end_game:
            self.p1.do_you_thing( self.board )
            if not self.board.is_end_game:
                self.p2.do_you_thing( self.board )
        return self.board.status
