import curses


class Player:
    def __init__( self, screen, piece ):
        self.piece = piece
        self.screen = screen

    def do_you_thing( self, board ):
        board.set_preview( self.piece )
        while True:
            board.draw()
            key = self.screen.getkey()
            if key == 'KEY_DOWN':
                board.down_preview()
            elif key == 'KEY_UP':
                board.up_preview()
            elif key == 'KEY_LEFT':
                board.left_preview()
            elif key == 'KEY_RIGHT':
                board.right_preview()
            elif key == curses.KEY_ENTER or key == '\n':
                board.choice_preview()
                break
