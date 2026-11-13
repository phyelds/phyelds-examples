"""The counter returns the updated round count as a plain integer."""

import unittest

from phyelds.vm.device import Device

from counter import counter


class CounterTest(unittest.TestCase):
    """Every device counts its own rounds."""

    def test_counter_returns_the_updated_count_each_round(self) -> None:
        """The first round returns 1, and every round one more."""
        device = Device(0, counter)

        results = []
        for _ in range(3):
            device.run_round({})
            results.append(device.result)

        self.assertEqual(results, [1, 2, 3])
        self.assertTrue(all(type(value) is int for value in results))


if __name__ == "__main__":
    unittest.main()
