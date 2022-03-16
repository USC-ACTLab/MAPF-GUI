import tkinter as tk


class HoverPool:
    def __init__(self, canvas):
        self.hoverpool = dict()
        self.canvas = canvas
        self.canvas.bind("<Motion>", self.check)

    def addWidget(self, target, tag, pos, **kwargs):
        self.hoverpool[tag] = target
        win = self.canvas.create_window(pos, window=target, **kwargs)
        self.canvas.itemconfig(win, tag=(tag))

    def check(self, event):
        if len(self.canvas.gettags('current')):
            for k, v in self.hoverpool.items():
                if k in self.canvas.gettags('current'):
                    v.focus_set()
                    return

        self.canvas.master.focus_set()


class App(tk.Tk):
    WIDTH, HEIGHT, TITLE = 800, 600, 'Application'

    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, background='red')
        self.canvas.pack(fill='both', expand=True, side='left')

        # init hoverpool
        hoverpool = HoverPool(self.canvas)

        self.frame1 = tk.Frame(self, background='green', height=50, width=50)
        self.frame1.bind('<Key-p>', self.onFrame1Action)
        self.frame1.bind('<Key-b>', self.onFrame1Action)

        # add frame1 to the hover pool
        hoverpool.addWidget(self.frame1, 'frame1', (50, 50), anchor='nw')

        self.frame2 = tk.Frame(self, background='green', height=50, width=50)
        self.frame2.bind('<Key-p>', self.onFrame2Action)
        self.frame2.bind('<Key-b>', self.onFrame2Action)

        # add frame2 to the hover pool
        hoverpool.addWidget(self.frame2, 'frame2', (105, 50), anchor='nw')

    def onFrame1Action(self, event):
        if event.char == 'p':
            self.frame1['background'] = 'purple'
        if event.char == 'b':
            self.frame1['background'] = 'black'

    def onFrame2Action(self, event):
        if event.char == 'p':
            self.frame2['background'] = 'pink'
        if event.char == 'b':
            self.frame2['background'] = 'blue'


if __name__ == '__main__':
    app = App()
    app.title(App.TITLE)
    app.geometry(f'{App.WIDTH}x{App.HEIGHT}')
    app.resizable(width=False, height=False)
    app.mainloop()