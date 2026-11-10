"""The counter returns the updated round count as a plain integer."""

from counter import counter
from phyelds.vm.device import Device


def test_counter_returns_the_updated_count_each_round():
    device = Device(0, counter)

    results = []
    for _ in range(3):
        device.run_round({})
        results.append(device.result)

    assert results == [1, 2, 3]
    assert all(type(value) is int for value in results)
