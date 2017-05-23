import numpy as np
import tkinter
from PIL import Image
from PIL import ImageTk


class Renderer(object):
    def __init__(self, ball, tray):
        self.ball = ball
        self.tray = tray

    def update(self):
        ball_position = self.ball.get_position()
        tray_position = self.tray.get_position()

        self.screen.fill(self.bg_code)
        self.screen[ball_position] = self.ball_code
        self.screen[tray_position] = self.tray_code


def button_click_exit_mainloop(event):
    event.widget.quit()  # this will cause mainloop to unblock.


class RGBRender(Renderer):
    def __init__(self, canvas, ball, tray, internal_render, debug=False):

        Renderer.__init__(self, ball, tray)

        self.screen = np.ndarray(shape=(*canvas.get_size(), 3), dtype=np.uint8)
        self.screen.fill(242)

        self.bg_code = (242, 242, 242)[0]
        self.ball_code = (231, 56, 133)
        self.tray_code = (55, 82, 159)

        self.internal_render = internal_render
        self.debug = debug

        if internal_render is True:
            self._init_internal_window()

    def get_screen(self):
        return self.screen

    def _init_internal_window(self):
        """ Sets window for internal renderer. """

        self.win = tkinter.Tk()
        self.win.geometry('+%d+%d' % (100, 100))
        self.win.title("Catcher")
        if self.debug:
            self.win.bind("<Button>", button_click_exit_mainloop)
        self.old_screen_label = None

    def render(self):
        """Opens a tk window and displays a PIL.Image"""

        screen = Image.fromarray(self.screen, 'RGB')
        screen = screen.resize((512, 512))
        self.win.geometry('%dx%d' % (screen.size[0], screen.size[1]))

        tkpi = ImageTk.PhotoImage(screen)
        label_img = tkinter.Label(self.win, image=tkpi)
        label_img.place(x=0, y=0,
                        width=screen.size[0], height=screen.size[1])

        if self.debug:
            self.win.mainloop()            # wait until user clicks the window
        self.win.update_idletasks()
        self.win.update()


class AsciiArtRender(Renderer):
    def __init__(self, canvas, ball, tray):
        Renderer.__init__(self, ball, tray)

        self.screen = np.ndarray(shape=canvas.get_size(), dtype=np.uint8)

        self.bg_code = 0
        self.ball_code = 1
        self.tray_code = 7

    def render(self):
        print(self.screen)
