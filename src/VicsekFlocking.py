"""
Vicsek flocking: 20 VMAS robots align their headings with their neighbours and
fly away as a single flock.
"""
import math

import torch
from vmas import make_env
from phyelds.calculus import aggregate, neighbors
from phyelds.libraries.device import store, sense
from phyelds.simulator import Simulator
from phyelds.simulator.effects import RenderConfig, RenderMode
from phyelds.simulator.neighborhood import radius_neighborhood
from phyelds.simulator.runner import schedule_program_for_all
from phyelds.vmas import VmasEnvironment, vmas_runner

from VMASRenderMonitor import VMASRenderMonitor

DURATION = 200.0
STEP = 1.0  # time between two physics steps, and between two rounds of a robot


def perturbation():
    angle = (torch.rand(1) * 2 - 1) * math.pi  # ~ U(-pi,pi)
    return angle


def mean_velocity(velocities):
    t = torch.stack(velocities)
    return torch.mean(t, dim=0).squeeze()


def velocity_to_angle(vel, avg_vel):
    eps = 1e-6
    if torch.norm(avg_vel) > eps:
        direction = avg_vel / torch.norm(avg_vel)
    else:
        vel_norm = torch.norm(vel)

        if vel_norm > eps:
            direction = vel / vel_norm
        else:
            theta_rand = torch.rand(1, device=vel.device) * 2 * math.pi
            direction = torch.stack([
                torch.cos(theta_rand),
                torch.sin(theta_rand)
            ])
    return torch.atan2(direction[1], direction[0])


@aggregate
def action():
    myself = sense('agent')
    vel = myself.state.vel.squeeze()
    neighbors_info = neighbors(vel).exclude_self()
    if neighbors_info:
        velocities = [vel for vel in neighbors_info.values()]
        avg_vel = mean_velocity(velocities)
        theta = velocity_to_angle(vel, avg_vel)
        noise = perturbation()
        theta = theta + 0.1 * noise
        next_vel = [torch.cos(theta).item(), torch.sin(theta).item()]
        store("action", next_vel)
    else:
        vel = vel.flatten().tolist()
        store("action", vel)


def build_simulator() -> Simulator:
    """The VMAS flocking scenario, with every robot running ``action``."""
    env = make_env(scenario="flocking", num_envs=1, n_agents=20, n_obstacles=0)
    simulator = Simulator(VmasEnvironment(env))
    simulator.environment.set_neighborhood_function(radius_neighborhood(1.0))
    schedule_program_for_all(simulator, 0.0, STEP, action)
    simulator.schedule_event(0.2, vmas_runner, simulator, STEP)
    return simulator


def main() -> None:
    """Run the flock and save it as a GIF, plus one PDF per frame."""
    simulator = build_simulator()
    VMASRenderMonitor(
        simulator,
        RenderConfig(effects=[], mode=RenderMode.SAVE, save_as="vicsek", dt=STEP),
    )
    simulator.run(DURATION)


if __name__ == "__main__":
    main()
