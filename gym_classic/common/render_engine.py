import numpy as np
import tkinter
from PIL import Image
from PIL import ImageTk


def button_click_exit_mainloop(event):
    event.widget.quit()  # this will cause mainloop to unblock.


class RGBRender:
    def __init__(self, win_name, canvas, entities, internal_render,
                 debug=False):

        self.win_name = win_name
        self.canvas = canvas
        self.entities = entities
        self.internal_render = internal_render
        self.debug = debug

        scale_factor = int(512 / max(canvas.size))
        self.height, self.width = [scale_factor * sz for sz in canvas.size]

        self.screen = np.ndarray(shape=(*canvas.size, 3), dtype=np.uint8)
        self.screen[:, :] = canvas.color

        if internal_render is True:
            self._init_internal_window()


    def update(self):
        self.__refresh_screen()

        for entity in self.entities:
            self.screen[entity.position] = entity.color


    def get_screen(self):
        return self.screen


    def _init_internal_window(self):
        """ Sets window for internal renderer. """

        self.win = tkinter.Tk()
        self.win.geometry('%dx%d' % (self.width, self.height))
        self.win.title(self.win_name)

        if self.debug:
            self.win.bind("<Button>", button_click_exit_mainloop)
        self.old_screen_label = None


    def render(self):
        """Opens a tk window and displays a PIL.Image"""

        screen = Image.fromarray(self.screen, 'RGB')
        screen = screen.resize((self.width, self.height))

        tkpi = ImageTk.PhotoImage(screen)
        label_img = tkinter.Label(self.win, image=tkpi)
        label_img.place(x=0, y=0, width=self.width, height=self.height)

        if self.debug:
            self.win.mainloop()            # wait until user clicks the window
        self.win.update_idletasks()
        self.win.update()

    def __refresh_screen(self):
        self.screen[:, :] = self.canvas.color


class SymbolicRender:
    def __init__(self, canvas, entities):
        self.canvas = canvas
        self.entities = entities
        self.screen = np.zeros(shape=canvas.size, dtype=np.uint8)


    def update(self):
        self.__refresh_screen()
        for entity in self.entities:
            self.screen[entity.position] = entity.code


    def get_screen(self):
        return self.screen


    def __refresh_screen(self):
        self.screen.fill(self.canvas.code)
