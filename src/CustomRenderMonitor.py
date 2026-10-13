"""
A RenderMonitor styled for papers: a square figure, large labels and a PDF of
the last frame.
"""
from pathlib import Path

from phyelds.simulator import Simulator
from phyelds.simulator.effects import RenderConfig, RenderMode
from phyelds.simulator.render import RenderMonitor


class CustomRenderMonitor(RenderMonitor):
    """
    Render the nodes like RenderMonitor, with a style readable in a paper.
    """

    def __init__(self, simulator: Simulator, config: RenderConfig):
        super().__init__(simulator, config)
        self.fig.set_size_inches(8, 8)

    def on_finish(self):
        if self.config.mode == RenderMode.SAVE:
            pdf = Path(self.config.save_as).with_suffix(".pdf")
            self.fig.savefig(pdf, dpi=500, bbox_inches="tight")
        super().on_finish()

    def _setup_axis(self):
        super()._setup_axis()
        if self.config.show_axis:
            if self.config.title:
                self.ax.set_title(self.config.title, fontsize=35)
            self.ax.set_xlabel("X(m)", fontsize=35)
            self.ax.set_ylabel("Y(m)", fontsize=35)
            self.ax.tick_params(labelsize=25)
