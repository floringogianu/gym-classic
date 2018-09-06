from .catcher_game import Catcher
from .sanity_checker_game import SanityChecker
from .blind_cliff_walk_game import BlindCliffWalk
from gym.envs.registration import register


ALL_GAMES = {
    "Catcher": Catcher,
    "SanityChecker": SanityChecker,
    "BlindCliffWalk": BlindCliffWalk
}


def get_game_module(game_name):
    return ALL_GAMES[game_name]


# Default
register(
    id='Catcher-v0',
    entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
    kwargs={'game_id': 'Catcher-v0', 'game_module': 'Catcher',
            'show_screen': False, 'level': 2},
    tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
    nondeterministic=False,
)

register(
    id='SanityChecker-v0',
    entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
    kwargs={'game_id': 'SanityChecker-v0', 'game_module': 'SanityChecker',
            'show_screen': False, 'level': 0},
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
                kwargs={'game_id': game, 'game_module': base_game,
                        'show_screen': False, 'level': level, 'width': size,
                        'height': size},
                tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
                nondeterministic=False,
            )

# Variable Length episodes of Catcher. Achieved by simply stalling the ball at
# each time-step with a probability between 0 and 0.6.
base_game = "Catcher"
for level in range(4):
    for size in (24, 32, 48):
        if size is 24:
            game = '%s-Level%d-VariableLength-v0' % (base_game, level)
        else:
            game = '%s-Level%d-x%d-VariableLength-v0' % (
                    base_game, level, size)

        register(
            id=game,
            entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
            kwargs={'game_id': game, 'game_module': base_game,
                    'show_screen': False, 'level': level, 'width': size,
                    'height': size, 'variable_length': True},
            tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
            nondeterministic=False,
        )

base_game = "BlindCliffWalk-v0"
register(
    id=base_game,
    entry_point='gym_fast_envs.gym_fast_envs:FastEnvs',
    kwargs={'game_id': base_game, 'game_module': 'BlindCliffWalk',
            'show_screen': False, 'N': 4},
    tags={'wrapper_config.TimeLimit.max_episode_steps': 10000},
    nondeterministic=False,
)
