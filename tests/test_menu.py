from unittest import TestCase
from unittest.mock import Mock
from menu import Menu


list_opcion = [ 'P1 vs CPU', 'P1 vs P2', 'CPU vs P2',
                'CPU vs CPU (Let the real players play!)', 'Exit' ]

class Test_menu( TestCase ):
    def test_init( self ):
        window = Mock()
        menu = Menu( window )
        for opcion in list_opcion:
            menu.add_opcion( opcion )

        self.assertEqual( len( menu.opcions ), 5 )
        self.assertEqual( menu.opcion_select, 0 )
        return menu

    def test_send_key_down( self ):
        menu = self.test_init()
        menu.send_key( 'KEY_DOWN' )
        self.assertEqual( menu.opcion_select, 1 )
        menu.send_key( 'KEY_DOWN' )
        self.assertEqual( menu.opcion_select, 2 )
        menu.send_key( 'KEY_DOWN' )
        self.assertEqual( menu.opcion_select, 3 )
        menu.send_key( 'KEY_DOWN' )
        self.assertEqual( menu.opcion_select, 4 )
        menu.send_key( 'KEY_DOWN' )
        self.assertEqual( menu.opcion_select, 0 )

    def test_send_key_up( self ):
        menu = self.test_init()
        menu.send_key( 'KEY_UP' )
        self.assertEqual( menu.opcion_select, 4 )
        menu.send_key( 'KEY_UP' )
        self.assertEqual( menu.opcion_select, 3 )
        menu.send_key( 'KEY_UP' )
        self.assertEqual( menu.opcion_select, 2 )
        menu.send_key( 'KEY_UP' )
        self.assertEqual( menu.opcion_select, 1 )
        menu.send_key( 'KEY_UP' )
        self.assertEqual( menu.opcion_select, 0 )

    def test_send_key_enter( self ):
        menu = self.test_init()
        response = menu.send_key( '\n' )
        self.assertEqual( response, 0 )
        menu.send_key( 'KEY_UP' )
        response = menu.send_key( '\n' )
        self.assertEqual( response, 4 )
