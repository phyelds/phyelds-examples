"""
Counter: the simplest stateful program, every device counts its own rounds.
"""
import random

from phyelds.calculus import aggregate, remember
from phyelds.simulator import Simulator
from phyelds.simulator.deployments import deformed_lattice
from phyelds.simulator.effects import DrawEdges, DrawNodes, RenderConfig, RenderMode
from phyelds.simulator.neighborhood import radius_neighborhood
from phyelds.simulator.render import RenderMonitor
from phyelds.simulator.runner import aggregate_program_runner

DURATION = 100.0


@aggregate
def counter() -> int:
    """The number of rounds this device has executed so far."""
    set_value, value = remember(0)
    set_value(value + 1)
    return value


def build_simulator() -> Simulator:
    """A 20x20 lattice whose devices start their rounds at slightly different times."""
    random.seed(42)
    simulator = Simulator()
    simulator.environment.set_neighborhood_function(radius_neighborhood(1.15))
    deformed_lattice(simulator, 20, 20, 1, 0.01)
    for node in simulator.environment.nodes.values():
        simulator.schedule_event(random.random() / 100, aggregate_program_runner, simulator, 1.1, node, counter)
    return simulator


def main() -> None:
    """Run the counter and save the video."""
    simulator = build_simulator()
    RenderMonitor(
        simulator,
        RenderConfig(
            effects=[DrawEdges(), DrawNodes(color_from="result")],
            mode=RenderMode.SAVE,
            save_as="counter.mp4",
            dt=0.1,
        ),
    )
    simulator.run(DURATION)


if __name__ == "__main__":
    main()
