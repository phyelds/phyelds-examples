"""
Regenerate the animations shown in the README, from the same simulations as the
examples:

    poetry run python src/readme_gifs.py
"""
from pathlib import Path

from PIL import Image, ImageSequence
from phyelds.simulator import Simulator
from phyelds.simulator.effects import DrawEdges, DrawNodes, RenderConfig, RenderMode
from phyelds.simulator.render import RenderMonitor

import channel
import scr

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FRAME_MILLISECONDS = 120  # playback speed of every GIF, whatever the simulated time


def record(simulator: Simulator, name: str, dt: float, duration: float, **draw_nodes) -> None:
    """
    Run ``simulator`` for ``duration`` and save one frame every ``dt`` to ``assets/<name>``.
    The ``draw_nodes`` options (e.g. ``cmap``, ``vmin``) go to ``DrawNodes``.
    """
    path = ASSETS / name
    RenderMonitor(
        simulator,
        RenderConfig(
            effects=[DrawEdges(alpha=0.3), DrawNodes(color_from="result", **draw_nodes)],
            mode=RenderMode.SAVE,
            save_as=str(path),
            dt=dt,
            show_axis=False,
        ),
    )
    simulator.run(duration)
    path.with_suffix(".png").unlink()  # RenderMonitor also saves the last frame
    _set_speed(path)


def _set_speed(path: Path) -> None:
    """Replay the GIF at FRAME_MILLISECONDS per frame, looping forever."""
    with Image.open(path) as gif:
        frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=FRAME_MILLISECONDS, loop=0)


def main() -> None:
    """Regenerate every animation used by the README."""
    ASSETS.mkdir(exist_ok=True)
    record(channel.build_simulator(), "channel.gif", dt=0.1, duration=5.0, cmap="plasma", vmin=0.0, vmax=1.0)
    record(scr.build_simulator(), "scr.gif", dt=1.0, duration=50.0, cmap="plasma")


if __name__ == "__main__":
    main()
