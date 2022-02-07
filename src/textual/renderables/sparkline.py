from __future__ import annotations

from typing import Sequence, Any, Iterable

from rich.color import Color
from rich.console import ConsoleOptions, Console, RenderResult
from rich.segment import Segment
from rich.style import Style


def blend_colors(color1: Color, color2: Color, ratio: float) -> Color:
    r1, g1, b1 = color1.triplet
    r2, g2, b2 = color2.triplet
    dr = r2 - r1
    dg = g2 - g1
    db = b2 - b1
    color = f"#{int(r1 + dr * ratio):02X}{int(g1 + dg * ratio):02X}{int(b1 + db * ratio):02X}"
    return Color.parse(color)


# TODO: Finish docstring, add docstring to function above
class Sparkline:
    """A sparkline representing a series of data.

    Args:
        data (Sequence[float]): The sequence of data to render.
        width (int, optional): The width of the sparkline/the number of buckets to partition the data into.
        min_color (Color, optional): The color
    """

    BARS = "▁▂▃▄▅▆▇█"

    def __init__(
        self,
        data: Sequence[float],
        width: int | None,
        min_color: Color | None = None,
        max_color: Color | None = None,
    ) -> None:
        self.data = data
        self.width = width
        self.min_color = Style.from_color(min_color or Color.from_rgb(0, 255, 0))
        self.max_color = Style.from_color(max_color or Color.from_rgb(255, 0, 0))

    def _split(self, data: Sequence[Any], num_buckets: int) -> Iterable[list]:
        num_steps, remainder = divmod(len(data), num_buckets)
        for i in range(num_buckets):
            start = i * num_steps + min(i, remainder)
            end = (i + 1) * num_steps + min(i + 1, remainder)
            yield data[start:end]

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        len_data = len(self.data)
        if len_data == 0:
            yield Segment("▁" * self.width, style=self.min_color)
            return
        if len_data == 1:
            yield Segment("█" * self.width, style=self.max_color)
            return

        minimum, maximum = min(self.data), max(self.data)
        extent = maximum - minimum or 1

        partitions = list(self._split(self.data, num_buckets=self.width))

        partition_index = 0
        bars_rendered = 0
        step = len_data / self.width
        while bars_rendered < self.width:
            partition = partitions[int(partition_index)]
            if not partition:
                yield Segment(text=self.BARS[0])
                bars_rendered += 1
                return
            partition_max = max(partition)
            height_ratio = (partition_max - minimum) / extent
            bar_index = int(height_ratio * (len(self.BARS) - 1))
            bar_color = blend_colors(
                self.min_color.color, self.max_color.color, height_ratio
            )
            yield Segment(text=self.BARS[bar_index], style=Style.from_color(bar_color))
            bars_rendered += 1
            partition_index += step


if __name__ == "__main__":
    console = Console()
    datasets = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        [0, 10, 0, 10],
        [100, 100, 100, 100, 100, 100, 100],
        [40],
    ]
    for ds in datasets:
        console.print(Sparkline(ds, width=30))
        console.print("\n")
