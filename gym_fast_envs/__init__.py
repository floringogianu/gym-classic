from .catcher_game import Catcher
from gym.envs.registration import registry, register, make, spec

# Default
register(
    id='Catcher-v0',
    entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
    kwargs={'game_name': 'Catcher-v0', 'display_screen': False, 'level': 2},
    tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
    nondeterministic=False,
)

# Difficulty levels and sizes
for level in range(6):
    for size in (24, 32, 48):
        if size is 24:
            game = 'Catcher-Level%d-v0' % (level)
        else:
            game = 'Catcher-Level%d-x%d-v0' % (level, size)

        register(
            id=game,
            entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
            kwargs={'game_name': game, 'display_screen': False,
                    'level': level, 'width': size, 'height': size},
            tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
            nondeterministic=False,
        )
