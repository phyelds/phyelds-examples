"""
Self-organising coordination regions (SCR): the network splits into areas, each
one with an elected leader, and every device learns the size of its area.
"""
import random

from phyelds.calculus import aggregate
from phyelds.libraries.collect import count_nodes
from phyelds.libraries.distances import neighbors_distances
from phyelds.libraries.leader_election import elect_leaders
from phyelds.libraries.spreading import broadcast, distance_to
from phyelds.simulator import Simulator
from phyelds.simulator.deployments import deformed_lattice
from phyelds.simulator.effects import RenderConfig, RenderMode
from phyelds.simulator.neighborhood import radius_neighborhood
from phyelds.simulator.runner import aggregate_program_runner

from CustomDrawings import CustomDrawEdges, CustomDrawNodes
from CustomRenderMonitor import CustomRenderMonitor

DURATION = 200.0
AREA_RADIUS = 4


@aggregate
def scr() -> int:
    """The number of devices in the area of the leader each device belongs to."""
    distances = neighbors_distances()
    leader = elect_leaders(AREA_RADIUS, distances)
    potential = distance_to(leader, distances)
    nodes = count_nodes(potential)
    return broadcast(leader, nodes, distances)


def build_simulator() -> Simulator:
    """A 20x20 lattice whose devices start their rounds at slightly different times."""
    random.seed(42)
    simulator = Simulator()
    simulator.environment.set_neighborhood_function(radius_neighborhood(1.15))
    deformed_lattice(simulator, 20, 20, 1, 0.01)
    for node in simulator.environment.nodes.values():
        simulator.schedule_event(random.random() / 100, aggregate_program_runner, simulator, 1.1, node, scr)
    return simulator


def main() -> None:
    """Run SCR and save the video, plus the last frame as a PDF."""
    simulator = build_simulator()
    CustomRenderMonitor(
        simulator,
        RenderConfig(
            effects=[CustomDrawEdges(), CustomDrawNodes(color_from="result")],
            mode=RenderMode.SAVE,
            save_as="scr.mp4",
            dt=0.1,
        ),
    )
    simulator.run(DURATION)


if __name__ == "__main__":
    main()
