import time
import numpy as np

from gym_fast_envs import Catcher
from gym_fast_envs import SanityChecker


if __name__ == '__main__':
    player_rng = np.random.RandomState(0)
    game = Catcher(width=24, height=24, variable_length=True, internal_render=True)
    # game = SanityChecker(width=24, height=24, internal_render=True)

    game.set_seed(23)  # test change of seed

    start = time.time()
    o, t, r = game.reset(), False, 0
    ep = 0
    step = 0
    tot_rw = 0
    ep_steps = 0

    while ep <= 19:
        o, t, r = game.step(game.actions[player_rng.choice(2)])
        step += 1
        ep_steps += 1
        game.display()
        tot_rw += r
        time.sleep(0.01)
        if t:
            ep += 1
            print(ep_steps)
            ep_steps = 0
            o, t, r = game.reset(), False, 0

    print("Finished %d episodes in %d steps in %.2fs. Total reward: %d." %
          (ep, step, time.time() - start, tot_rw))
