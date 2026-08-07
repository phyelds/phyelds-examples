# Phyelds Examples

Runnable examples for `phyelds` 7.x, including a VMAS-based Vicsek flocking
simulation.

## Setup

```bash
poetry install
```

The examples use `phyelds>=7.0.0,<8.0.0`. The VMAS example additionally uses
`phyelds-vmas`, which provides the `phyelds.vmas` integration namespace.

## Run Examples

Run a core simulator example:

```bash
poetry run python src/counter.py
```

Run the VMAS Vicsek flocking example:

```bash
poetry run python src/VicsekFlocking.py
```

VMAS-specific types are imported separately from the generic simulator:

```python
from phyelds.simulator import Simulator
from phyelds.simulator.runner import schedule_program_for_all
from phyelds.vmas import VmasEnvironment, vmas_runner
```

The Binder notebook installs the core package only because it contains no VMAS
examples.
