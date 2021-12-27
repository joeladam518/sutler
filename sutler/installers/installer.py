from abc import ABC
from ..application import App
from click.core import Context as ClickContext


class Installer(ABC):
    def __init__(self, ctx: ClickContext):
        self.app: App = ctx.find_root().obj or App()
        self.ctx: ClickContext = ctx
