"""
Channel: the devices on the shortest path between a source and a target
self-organise into a band.
"""
import random

from phyelds.calculus import aggregate
from phyelds.libraries.collect import collect_or
from phyelds.libraries.device import sense
from phyelds.libraries.distances import neighbors_distances
from phyelds.libraries.spreading import distance_to
from phyelds.simulator import Simulator
from phyelds.simulator.deployments import deformed_lattice
from phyelds.simulator.effects import RenderConfig, RenderMode
from phyelds.simulator.neighborhood import radius_neighborhood
from phyelds.simulator.runner import aggregate_program_runner

from CustomDrawings import CustomDrawEdges, CustomDrawNodes
from CustomRenderMonitor import CustomRenderMonitor

DURATION = 10.0
CHANNEL_WIDTH = 1.12


@aggregate
def channel() -> float:
    """1.0 on the devices close to the path from the source to the target, 0.0 elsewhere."""
    distances = neighbors_distances()
    target_distance = distance_to(sense("target"), distances)
    nodes_in_path = collect_or(target_distance, sense("source"))
    distance_from_path = distance_to(nodes_in_path, distances)
    return 1.0 if distance_from_path < CHANNEL_WIDTH else 0.0


def build_simulator() -> Simulator:
    """A 20x20 lattice with the source in a corner and the target in the opposite one."""
    random.seed(42)
    simulator = Simulator()
    simulator.environment.set_neighborhood_function(radius_neighborhood(1.12))
    deformed_lattice(simulator, 20, 20, 1, 0.01)
    for node in simulator.environment.nodes.values():
        node.data = {"source": False, "target": False}
    simulator.environment.node_list()[0].data["source"] = True
    simulator.environment.node_list()[-1].data["target"] = True
    for node in simulator.environment.nodes.values():
        simulator.schedule_event(0.0, aggregate_program_runner, simulator, 0.1, node, channel)
    return simulator


def main() -> None:
    """Run the channel and save the video, plus the last frame as a PDF."""
    simulator = build_simulator()
    CustomRenderMonitor(
        simulator,
        RenderConfig(
            effects=[CustomDrawEdges(), CustomDrawNodes(color_from="result")],
            mode=RenderMode.SAVE,
            save_as="channel.mp4",
            dt=0.1,
        ),
    )
    simulator.run(DURATION)


if __name__ == "__main__":
    main()
