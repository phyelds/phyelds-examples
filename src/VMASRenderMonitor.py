import imageio
from PIL import Image
from phyelds.simulator import Simulator, Monitor
from phyelds.simulator.effects import RenderConfig


class VMASRenderMonitor(Monitor):
    """
    Grab one VMAS frame every ``config.dt``; at the end, save them as a GIF and
    one PDF per frame.
    """

    def __init__(self, simulator: Simulator, config: RenderConfig):
        super().__init__(simulator)
        self.config = config
        self.simulator = simulator
        self.frames = []
        self.last_render_time = 0.0

    def update(self):
        if self.simulator.current_time - self.last_render_time < self.config.dt:
            return
        self.frames.append(self.simulator.environment.vmas_environment.render(mode="rgb_array"))
        self.last_render_time = self.simulator.current_time

    def on_finish(self):
        imageio.mimsave(f"{self.config.save_as}.gif", self.frames, fps=20)

        for index, frame in enumerate(self.frames):
            img = Image.fromarray(frame)
            name = f'frame-{index:04d}.pdf'
            img.save(name, resolution=500)
