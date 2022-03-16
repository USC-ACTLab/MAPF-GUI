import PySimpleGUI as sg
from random import randint

MAX_ROWS = 10
MAX_COL = 10
board = [[0 for j in range(MAX_COL)] for i in range(MAX_ROWS)]
color = ['black', 'red', 'green']
layout =  [[sg.Button('', size=(2, 2), key=(j,i), pad=(0,0), tooltip=f"{j},{i}", button_color='white') for j in range(MAX_COL)] for i in range(MAX_ROWS-1, -1, -1)]

window = sg.Window('Minesweeper', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    # window[(row, col)].update('New text')   # To change a button's text, use this pattern
    # For this example, change the text of the button to the board's value and turn color black

    window[event].update('', button_color=color[board[event[1]][event[0]] % 3])

    board[event[1]][event[0]] += 1
    print(event)
window.close()