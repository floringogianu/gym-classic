import time
import numpy as np

from gym_fast_envs import Catcher


if __name__ == '__main__':
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

    print("Finished %d episodes in %d steps in %.2fs. Total reward: %d." %
          (ep, step, time.time() - start, tot_rw))
