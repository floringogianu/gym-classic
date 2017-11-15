from .catcher_game import Catcher
from .sanity_checker_game import SanityChecker
from gym.envs.registration import register


ALL_GAMES = {
    "Catcher": Catcher,
    "SanityChecker": SanityChecker
}


def get_game_module(game_name):
    return ALL_GAMES[game_name]


# Default
register(
    id='Catcher-v0',
    entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
    kwargs={'game_name': 'Catcher', 'display_screen': False, 'level': 2},
    tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
    nondeterministic=False,
)

register(
    id='SanityChecker-v0',
    entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
    kwargs={'game_name': 'SanityChecker', 'display_screen': False,
            'level': 0},
    tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
    nondeterministic=False,
)

# Difficulty levels and sizes
for base_game in ['Catcher', 'SanityChecker']:
    for level in range(4):
        for size in (24, 32, 48):
            if size is 24:
                game = '%s-Level%d-v0' % (base_game, level)
            else:
                game = '%s-Level%d-x%d-v0' % (base_game, level, size)

            register(
                id=game,
                entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
                kwargs={'game_name': base_game, 'display_screen': False,
                        'level': level, 'width': size, 'height': size},
                tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
                nondeterministic=False,
            )
