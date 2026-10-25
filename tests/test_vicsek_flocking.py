"""Run the Vicsek example without opening a display."""

import unittest
from unittest.mock import patch

import torch

from phyelds.vmas import action, agent
from VicsekFlocking import build_simulator


class VicsekFlockingTest(unittest.TestCase):
    """The example shares its typed devices with the VMAS host."""

    def test_flocking_uses_shared_devices_each_round(self) -> None:
        """Every robot uses the shared objects each round."""
        torch.manual_seed(0)
        simulator = build_simulator()

        with (
            patch.object(agent, "sense", wraps=agent.sense) as readings,
            patch.object(action, "send", wraps=action.send) as actions,
        ):
            simulator.run(1.3)

        self.assertEqual(readings.call_count, 40)
        self.assertEqual(actions.call_count, 40)
        for node in simulator.environment.node_list():
            value = action.read(node.data["outputs"])
            self.assertEqual(len(value), 2)
            self.assertTrue(torch.isfinite(torch.tensor(value)).all())


if __name__ == "__main__":
    unittest.main()
