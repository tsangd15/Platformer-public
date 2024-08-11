"""Module to house functions used by multiple classes"""


def check_alignment(alignment):
    """Function to check if an input alignment is valid."""
    # +-------------+---------------+--------------+
    # | top_left    | top_center    | top_right    |
    # +-------------+---------------+--------------+
    # | middle_left | middle_center | middle_right |
    # +-------------+---------------+--------------+
    # | bottom_left | bottom_center | bottom_right |
    # +-------------+---------------+--------------+

    valid_alignments = ["top_left", "top_center", "top_right",
                        "middle_left", "middle_center", "middle_right",
                        "bottom_left", "bottom_center", "bottom_right"]

    if alignment in valid_alignments:
        return alignment

    # raise exception if not in valid_alignments
    raise Exception("Invalid alignment argument given.")


def align(alignment, rect, startx, starty):
    """Function to align a sprite using an alignment relative to a point
    (startx, starty)."""
    if alignment == "top_left":
        rect.topleft = startx, starty
    elif alignment == "top_center":
        rect.centerx, rect.y = startx, starty
    elif alignment == "top_right":
        rect.topright = startx, starty
    elif alignment == "middle_left":
        rect.midleft = startx, starty
    elif alignment == "middle_center":
        rect.center = startx, starty
    elif alignment == "middle_right":
        rect.midright = startx, starty
    elif alignment == "bottom_left":
        rect.bottomleft = startx, starty
    elif alignment == "bottom_center":
        rect.centerx, rect.bottom = startx, starty
    else:
        rect.bottomright = startx, starty
