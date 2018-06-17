from baselines import deepq

from gym_env import Mega3TEnv


def callback(lcl, _glb):
    # stop training if the last 100 games were won
    is_solved = lcl['t'] > 100 and \
        sum(lcl['episode_rewards'][-101:-1]) / 100 >= 99
    return is_solved


def main():
    env = Mega3TEnv()
    model = deepq.models.mlp([64])
    act = deepq.learn(
        env,
        q_func=model,
        lr=1e-3,
        max_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10,
        callback=callback
    )
    print("Saving model to mega3t_model.pkl")
    act.save("mega3t_model.pkl")


if __name__ == '__main__':
    main()
