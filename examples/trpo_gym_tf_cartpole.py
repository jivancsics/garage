import gym

from garage.baselines import LinearFeatureBaseline
from garage.envs import normalize
from garage.envs.util import spec
from garage.misc.instrument import run_experiment_lite
from garage.misc.instrument import stub
from garage.tf.algos import TRPO
from garage.tf.envs import TfEnv
from garage.tf.policies import CategoricalMLPPolicy

stub(globals())

# Need to wrap in a tf environment and force_reset to true
# see https://github.com/openai/rllab/issues/87#issuecomment-282519288
env = TfEnv(gym.make("CartPole-v0"))

policy = CategoricalMLPPolicy(
    name="policy", env_spec=spec(env), hidden_sizes=(32, 32))

baseline = LinearFeatureBaseline(env_spec=spec(env))

algo = TRPO(
    env=env,
    policy=policy,
    baseline=baseline,
    batch_size=4000,
    max_path_length=200,
    n_itr=120,
    discount=0.99,
    step_size=0.01,
)

run_experiment_lite(algo.train(), n_parallel=1, snapshot_mode="last", seed=1)
