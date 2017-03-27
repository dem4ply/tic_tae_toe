import curses
from menu import Menu
from board import Board
from player import Player
from round import Round
from ai import AI


ai_tree = {}


list_opcion = [ 'P1 vs CPU', 'P1 vs P2', 'CPU vs P2',
                'CPU vs CPU (Let the real players play!)', 'Exit' ]


def draw_score( score, who_win ):
    clear_score( score )
    if who_win == 0:
        score.addstr( 1, 1, "Tie" )
    elif who_win == 1:
        score.addstr( 1, 1, "Player 1 win" )
    elif who_win == 2:
        score.addstr( 1, 1, "Player 2 win" )
    else:
        score.addstr( 1, 1, str( who_win ) )
    score.refresh()

def clear_score( score ):
    score.clear()
    score.border()
    score.refresh()


def p1_vs_cpu( screen, board ):
    board.clean_pieces()
    board.draw()
    p1 = Player( screen, board.X )
    p2 = AI( ai_tree, 2 )
    r = Round( p1, p2, board )
    who_win = r.start()
    board.preview_piece = None
    board.draw()
    return who_win


def p1_vs_p2( screen, board ):
    board.clean_pieces()
    board.draw()
    p1 = Player( screen, board.X )
    p2 = Player( screen, board.O )
    r = Round( p1, p2, board )
    who_win = r.start()
    board.preview_piece = None
    board.draw()
    return who_win


def cpu_vs_p2( screen, board ):
    board.clean_pieces()
    board.draw()
    p1 = AI( ai_tree, 1 )
    p2 = Player( screen, board.O )
    r = Round( p1, p2, board )
    who_win = r.start()
    board.preview_piece = None
    board.draw()
    return who_win


def cpu_vs_cpu( screen, board ):
    board.clean_pieces()
    board.draw()
    p1 = AI( ai_tree, 1 )
    p2 = AI( ai_tree, 2 )
    r = Round( p1, p2, board )
    who_win = r.start()
    board.preview_piece = None
    board.draw()
    return who_win


def main( screen ):
    curses.init_pair( 1, curses.COLOR_RED, curses.COLOR_BLACK )
    curses.init_pair( 2, curses.COLOR_GREEN, curses.COLOR_BLACK )
    curses.init_pair( 3, curses.COLOR_BLUE, curses.COLOR_BLACK )

    score = curses.newwin( 3, 42, 1, 1 )
    menu = curses.newwin( 7, 42, 4, 1 )
    board = curses.newwin( 8, 13, 4, 43 )

    menu = Menu( menu )
    for opcion in list_opcion:
        menu.add_opcion( opcion )

    board = Board( board )


    #screen.addstr("Pretty text", curses.color_pair(2))
    screen.refresh()
    menu.refresh()
    board.draw()
    #win.refresh()


    #screen.refresh()
    while True:
        key = screen.getkey()
        if key == curses.KEY_CLOSE:
            break
        elif key == ord( 'q' ):
            break
        opcion_select = menu.send_key( key )
        if opcion_select is not None:
            if opcion_select == 0:
                clear_score( score )
                who_win = p1_vs_cpu( screen, board )
                draw_score( score, who_win )
            if opcion_select == 1:
                clear_score( score )
                who_win = p1_vs_p2( screen, board )
                draw_score( score, who_win )
            if opcion_select == 2:
                clear_score( score )
                who_win = cpu_vs_p2( screen, board )
                draw_score( score, who_win )
            if opcion_select == 3:
                clear_score( score )
                who_win = cpu_vs_cpu( screen, board )
                draw_score( score, who_win )
            if opcion_select == 4:
                break
        menu.refresh()


if __name__ == '__main__':
    try:
        curses.wrapper( main )
    except Exception as e:
        import pdb
        pdb.post_mortem( e.__traceback__ )
