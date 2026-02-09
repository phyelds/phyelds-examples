import random

from phyelds.calculus import aggregate
from phyelds.calculus import remember
from phyelds.simulator import Simulator
from phyelds.simulator.deployments import deformed_lattice
from phyelds.simulator.effects import DrawNodes, DrawEdges, RenderConfig, RenderMode
from phyelds.simulator.neighborhood import radius_neighborhood
from phyelds.simulator.render import RenderMonitor
from phyelds.simulator.runner import aggregate_program_runner

random.seed(42)

@aggregate
def main():
    """
    Example to use the phyelds library to create a simple simulation
    :return:
    """
    set_value, value = remember(0)
    print(value)
    set_value(value+1)
    return value

simulator = Simulator()
# deformed lattice
simulator.environment.set_neighborhood_function(radius_neighborhood(1.15))
deformed_lattice(simulator, 20, 20, 1, 0.01)

for node in simulator.environment.nodes.values():
    simulator.schedule_event(random.random() / 100, aggregate_program_runner, simulator, 1.1, node, main)
# render
RenderMonitor(
    simulator,
    RenderConfig(
        effects=[DrawEdges(), DrawNodes(color_from="result")],
        mode=RenderMode.SAVE,
        save_as="counter.mp4",
        dt=0.1
    )
)
simulator.run(100)