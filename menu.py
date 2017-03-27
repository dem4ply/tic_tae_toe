import curses


class Menu:
    def __init__( self, windows ):
        self.opcions = []

        self.opcion_select = 0
        self.windows = windows

        self.debug = ''

    def add_opcion( self, string ):
        self.opcions.append( string )

    def send_key( self, key ):
        #self.debug = "{} {}".format(key, key == 'KEY_DOWN' )
        if key == 'KEY_DOWN':
            self.opcion_select += 1
            if self.opcion_select >= len( self.opcions ):
                self.opcion_select = 0
        elif key == 'KEY_UP':
            self.opcion_select -= 1
            if self.opcion_select < 0:
                self.opcion_select = len( self.opcions ) - 1
        elif key == 'KEY_LEFT':
            pass
        elif key == 'KEY_RIGHT':
            pass
        elif key == curses.KEY_ENTER or key == '\n':
            return self.opcion_select

    def refresh( self ):
        self.windows.clear()
        self.windows.border()

        for y, opcion in enumerate( self.opcions ):
            opcion = opcion
            if y == self.opcion_select:
                attr = self.get_attribute_for_selected()
            else:
                attr = self.get_attribute_for_unselected()

            self.windows.addstr( y + 1, 1, opcion, attr )

        self.windows.refresh()

    def get_attribute_for_selected( self ):
        return curses.A_REVERSE

    def get_attribute_for_unselected( self ):
        return curses.A_NORMAL
