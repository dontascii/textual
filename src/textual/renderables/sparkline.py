from __future__ import annotations

from typing import Sequence

from rich.console import ConsoleOptions, Console, RenderResult


class Sparkline:
    """A sparkline representing a series of data.

    Args:
        data (Sequence[float]): The sequence of data to render.
        width (int, optional): The width of the sparkline/the number of buckets to partition the data into.
    """

    def __init__(self, data: Sequence[float], width: int | None) -> None:
        self.data = data
        self.width = width

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        pass
