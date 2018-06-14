# This doesn't work. After 150 iterations still didn't learn anything.
import gym

from garage.algos import TRPO
from garage.baselines import LinearFeatureBaseline
from garage.envs import normalize
from garage.envs.util import horizon, spec
from garage.misc.instrument import run_experiment_lite
from garage.policies import CategoricalMLPPolicy


def run_task(*_):
    env = normalize(gym.make("MountainCar-v0"))

    policy = CategoricalMLPPolicy(env_spec=spec(env), hidden_sizes=(32, 32))

    baseline = LinearFeatureBaseline(env_spec=spec(env))

    algo = TRPO(
        env=env,
        policy=policy,
        baseline=baseline,
        batch_size=4000,
        max_path_length=horizon(env),
        n_itr=150,
        discount=0.99,
        step_size=0.1,
        plot=True,
    )
    algo.train()


run_experiment_lite(
    run_task,
    n_parallel=1,
    snapshot_mode="last",
    plot=True,
)
