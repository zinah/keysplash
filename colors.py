from __future__ import annotations

RGBColor = tuple[int, int, int]
NoteName = str
Octave = int
Note = tuple[NoteName, Octave]

# TODO what to do if gradient color not found?
def get_key_color(gradient: list(RGBColor), key: Note) -> RGBColor:
    return gradient[key]


# TODO make a better gradient - maybe rainbow?
def linear_gradient(
    start_color: RGBColor, end_color: RGBColor, n: int
) -> list(RGBColor):
    """
    Returns a gradient list of n colors between RGB colors.
    """

    def next_color_value(start_color_value, end_color_value, step, n):
        return int(
            start_color_value +
            step / (n - 1) * (end_color_value - start_color_value)
            )

    gradient = []
    for i in range(0, n):
        r = next_color_value(start_color[0], end_color[0], i, n)
        g = next_color_value(start_color[1], end_color[1], i, n)
        b = next_color_value(start_color[2], end_color[2], i, n)
        gradient.append((r, g, b))

    return gradient