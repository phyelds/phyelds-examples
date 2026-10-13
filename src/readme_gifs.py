"""
Regenerate the animations shown in the README, from the same simulations as the
examples:

    poetry run python src/readme_gifs.py
"""
from pathlib import Path

import torch
from PIL import Image, ImageSequence
from phyelds.simulator import Simulator
from phyelds.simulator.effects import DrawEdges, DrawNodes, RenderConfig, RenderMode
from phyelds.simulator.render import RenderMonitor

import channel
import scr
import VicsekFlocking
from VMASRenderMonitor import VMASRenderMonitor

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FRAME_MILLISECONDS = 120  # playback speed of every GIF, whatever the simulated time
VMAS_SIZE = 320  # side in pixels of the VMAS animation, rendered at 700
VMAS_COLORS = 32  # VMAS draws a fine grid that compresses badly: a small palette keeps the GIF light


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


class _ReadmeVmasMonitor(VMASRenderMonitor):
    """Grab the frames like VMASRenderMonitor, but save only a small GIF, every other frame."""

    def on_finish(self):
        frames = [_shrink(Image.fromarray(frame)) for frame in self.frames[::2]]
        _save_gif(Path(self.config.save_as), frames)


def _shrink(frame: Image.Image) -> Image.Image:
    """Resize a VMAS frame to VMAS_SIZE and reduce it to VMAS_COLORS colours."""
    small = frame.resize((VMAS_SIZE, VMAS_SIZE), Image.Resampling.LANCZOS)
    return small.quantize(colors=VMAS_COLORS, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)


def record_vicsek(name: str) -> None:
    """Run the Vicsek flock and save it to ``assets/<name>``."""
    torch.manual_seed(42)
    simulator = VicsekFlocking.build_simulator()
    _ReadmeVmasMonitor(simulator, RenderConfig(save_as=str(ASSETS / name), dt=VicsekFlocking.STEP))
    simulator.run(VicsekFlocking.DURATION)


def _set_speed(path: Path) -> None:
    """Replay the GIF at FRAME_MILLISECONDS per frame."""
    with Image.open(path) as gif:
        frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    _save_gif(path, frames)


def _save_gif(path: Path, frames: list[Image.Image]) -> None:
    """Save ``frames`` as a GIF at FRAME_MILLISECONDS per frame, looping forever."""
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=FRAME_MILLISECONDS, loop=0)


def main() -> None:
    """Regenerate every animation used by the README."""
    ASSETS.mkdir(exist_ok=True)
    record(channel.build_simulator(), "channel.gif", dt=0.1, duration=5.0, cmap="plasma", vmin=0.0, vmax=1.0)
    record(scr.build_simulator(), "scr.gif", dt=1.0, duration=50.0, cmap="plasma")
    record_vicsek("vicsek.gif")


if __name__ == "__main__":
    main()
