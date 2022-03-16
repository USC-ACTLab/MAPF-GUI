import PySimpleGUI as sg

layout = [[sg.Text('Window1')],
          [sg.Button('Ok')]]


def create_window():
    layout = [[sg.Button('Huh?')]]
    return sg.Window('NewWin', layout, finalize=True)


window1 = sg.Window('Ori', layout, finalize=True)
window1['Ok'].bind('<Enter><r>', 'Fuck yeah!')
window2 = None
event2 = None

while True:
    # window, event, value = sg.read_all_windows()
    event, value = window1.read()
    if window2:
        event2, value2 = window2.read()

    if event == 'Ok' and not window2:
        window2 = create_window()

    if event == sg.WIN_CLOSED:
        break

    if event2 == sg.WIN_CLOSED:
        window2 = None

    if event == 'OkFuck yeah!':
        window1['Ok'].click()
    print(event, value)


window1.close()
