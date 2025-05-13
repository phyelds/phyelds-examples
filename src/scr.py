import os
import glob
import random
from phyelds.calculus import aggregate, neighbors_distances
from phyelds.libraries.leader_election import elect_leader
from phyelds.libraries.spreading import distance_to
from phyelds.simulator import Simulator
from phyelds.simulator.deployments import deformed_lattice
from phyelds.simulator.neighborhood import radius_neighborhood
from phyelds.simulator.render import render_sync
from phyelds.simulator.runner import aggregate_program_runner
from phyelds.libraries.collect import count_nodes
from phyelds.libraries.spreading import broadcast
from phyelds.libraries.device import local_position, sense


random.seed(42)


@aggregate
def main():
    """
    Example to use the phyelds library to create a simple simulation
    :return:
    """
    distances = neighbors_distances(local_position())
    leader = elect_leader(4, distances)
    potential = distance_to(leader, distances)
    nodes = count_nodes(potential)
    area_value = broadcast(leader, nodes, distances)
    return area_value


# simulator = Simulator()
# # deformed lattice
# simulator.environment.set_neighborhood_function(radius_neighborhood(1.5))
# deformed_lattice(simulator, 10, 10, 1, 0.01)
# # put source
# for node in simulator.environment.nodes.values():
#     node.data = {"source": False, "target": False}
# # put a source in the first node
# simulator.environment.node_list()[0].data["source"] = True
# target = simulator.environment.node_list()[-1]
# target.data["target"] = True
# # schedule the main function
# for node in simulator.environment.nodes.values():
#     simulator.schedule_event(0.0, aggregate_program_runner, simulator, 0.1, node, main)
# # render
# simulator.schedule_event(1.0, render_sync, simulator, "result")
# simulator.run(100)

simulator = Simulator()
# deformed lattice
simulator.environment.set_neighborhood_function(radius_neighborhood(1.15))
deformed_lattice(simulator, 10, 10, 1, 0.01)
# put source
for node in simulator.environment.nodes.values():
    node.data = {"source": False, "target": False}
# put a source in the first node
simulator.environment.node_list()[0].data["source"] = True
target = simulator.environment.node_list()[-1]
target.data["target"] = True
# schedule the main function
for node in simulator.environment.nodes.values():
    simulator.schedule_event(0.0, aggregate_program_runner, simulator, 0.1, node, main)
# render
simulator.schedule_event(1.0, render_sync, simulator, "result")
simulator.run(100)