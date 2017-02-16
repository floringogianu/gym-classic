import numpy as np


class Ball(object):
    def __init__(self, bounds, level, rng):
        self.rng = rng

        self.x_bounds = (0, bounds[1])
        self.y_bounds = (0, bounds[0])

        self.x = int(np.floor(self.x_bounds[1] / 2))
        self.y = -1                                 # always starts at the top

        self.level = level
        self.angle = int(self.rng.choice([-1, 1]) * np.floor(self.level / 2))
        self.att_prob = self.level/10

    def move_ball(self):
        self.y += 1
        if self.rng.uniform() < 1 - self.att_prob:
            self.x += self.angle
        else:
            # attenuate angle
            self.x += self.angle + 1 if self.angle < 0 else self.angle - 1

        if self.x >= self.x_bounds[1]:
            self.x = self.x_bounds[1]
            self.angle = -self.angle
        elif self.x < 2 and self.angle <= 0:
            self.x = 0
            self.angle = -self.angle

    def get_position(self):
        return (self.y, self.x)

    def reset_position(self):
        self.x = self.rng.choice(self.x_bounds[1])
        self.y = -1                                 # always starts at the top


class Tray(object):
    def __init__(self, bounds):

        self.width = 2 if bounds[1] <= 24 else int(np.floor(bounds[1] / 8))

        self.x_bounds = (0, bounds[1])
        self.y_bounds = (bounds[0], bounds[0])  # stays at the bottom

        self.x = int(np.floor(self.x_bounds[1] / 2 - self.width))
        self.y = self.y_bounds[0]

    def move_tray(self, action):
        if action == -1:
            self.x = max(self.x - 1, 0)
        elif action == 1:
            self.x = min(self.x + 1, self.x_bounds[1] - self.width)

    def get_position(self):
        return (self.y, range(self.x, self.x+self.width+1))

    def reset_position(self):
        self.x = int(np.floor((self.x_bounds[1] - self.width) / 2 - 1))
        self.y = self.y_bounds[0]


class Canvas(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_bounds(self):
        return (self.height-1, self.width-1)            # numpy row-major order

    def get_size(self):
        return (self.height, self.width)


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


class AsciiArtRender(Renderer):
    def __init__(self, canvas, ball, tray):
        Renderer.__init__(self, ball, tray)

        self.screen = np.ndarray(shape=canvas.get_size(), dtype=np.uint8)

        self.bg_code = 0
        self.ball_code = 1
        self.tray_code = 7

    def render(self):
        print(self.screen)


def button_click_exit_mainloop(event):
    event.widget.quit()  # this will cause mainloop to unblock.


class RGBRender(Renderer):
    def __init__(self, canvas, ball, tray, internal_render):

        Renderer.__init__(self, ball, tray)

        self.screen = np.ndarray(shape=(*canvas.get_size(), 3), dtype=np.uint8)
        self.screen.fill(242)

        self.bg_code = (242, 242, 242)[0]
        self.ball_code = (231, 56, 133)
        self.tray_code = (55, 82, 159)

        self.internal_render = internal_render

        if internal_render is True:
            self._init_internal_window()

    def get_screen(self):
        return self.screen

    def _init_internal_window(self):
        """ Sets window for internal renderer. """
        print("Setting up tkinter...")

        self.win = tkinter.Tk()
        self.win.geometry('+%d+%d' % (100, 100))
        self.win.title("Catcher")
        # self.win.bind("<Button>", button_click_exit_mainloop)
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

        # self.win.mainloop()            # wait until user clicks the window
        self.win.update_idletasks()
        self.win.update()


class Catcher(object):
    def __init__(self, level=0, width=24, height=24, seed=42,
                 internal_render=False):

        self.seed = seed
        self.rng = np.random.RandomState(self.seed)

        self.level = level
        self.width = width
        self.height = height
        self.actions = (-1, 0, 1)

        self.positive_reward = 1
        self.negative_reward = 0

        self.internal_render = internal_render

        self._init()

    def _init(self):
        self.canvas = Canvas(self.width, self.height)
        self.tray = Tray(self.canvas.get_bounds())
        self.ball = Ball(self.canvas.get_bounds(), self.level, self.rng)

        if hasattr(self, "render_engine") and self.internal_render:
            self.render_engine.win.destroy()
        self.render_engine = RGBRender(self.canvas, self.ball, self.tray,
                                       self.internal_render)

        # self.render_engine=AsciiArtRender(self.canvas,self.ball,self.tray)

    def reset(self):
        self.tray.reset_position()
        self.ball.reset_position()

        return self.get_screen(), self.is_terminal(), self.get_reward()

    def set_seed(self, seed):
        self.seed = seed
        self.rng = np.random.RandomState(self.seed)

        # reset the state of the game
        self._init()

    def get_action_set(self):
        return self.actions

    def get_screen_dims(self):
        return self.canvas.get_size()

    def display(self):
        if self.internal_render:
            time.sleep(0.01)
            self.render_engine.render()

    def get_screen(self):
        return self.render_engine.get_screen()

    def step(self, action):
        self.ball.move_ball()
        self.tray.move_tray(self.actions[action])
        self.render_engine.update()

        return self.get_screen(), self.is_terminal(), self.get_reward()

    def get_reward(self):
        b_y, b_x = self.ball.get_position()
        t_y, t_x = self.tray.get_position()

        if not self.is_terminal():
            return 0
        else:
            if b_x < t_x.start or b_x > (t_x.stop-1):
                return self.negative_reward
            else:
                return self.positive_reward

    def is_terminal(self):
        b_y, b_x = self.ball.get_position()
        t_y, t_x = self.tray.get_position()

        return True if b_y == t_y else False


if __name__ == '__main__':

    import time
    import tkinter
    from PIL import Image
    from PIL import ImageTk

    player_rng = np.random.RandomState(0)
    game = Catcher(width=24, height=24, internal_render=True)

    game.set_seed(23)  # test change of seed

    start = time.time()
    o, t, r = game.reset()
    ep = 0
    step = 0
    tot_rw = 0

    while ep <= 10:
        o, t, r = game.step(game.actions[player_rng.choice(3)])
        step += 1
        game.display()
        tot_rw += r
        if t:
            ep += 1
            o, t, r = game.reset()

    print("Finished %d episodes in %d steps in %.2f. Total reward: %d.",
          (ep, step, time.time() - start, tot_rw))
