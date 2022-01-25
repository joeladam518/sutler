from abc import ABC
from click.core import Context as ClickContext
from ..app import App


class Provisioner(ABC):
    def __init__(self, ctx: ClickContext):
        self.app: App = ctx.find_root().obj or App()
        self.ctx: ClickContext = ctx
