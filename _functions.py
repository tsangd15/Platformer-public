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


def set_button_idle(button_group, button_text):
    """Function to find a button in a button sprite group and set it to idle
    state."""
    for button in button_group:
        if button.text == button_text:
            button.state_idle()
            return


def set_button_hover(button_group, button_text):
    """Function to find a button in a button sprite group and set it to hover
    state."""
    for button in button_group:
        if button.text == button_text:
            button.state_hover()
            return


def set_button_click(button_group, button_text):
    """Function to find a button in a button sprite group and set it to click
    state."""
    for button in button_group:
        if button.text == button_text:
            button.state_click()
            return


def is_point_within_rect(point, sprite):
    """Check if a point is within a pygame sprite's dimensions.
    Tuple/list in form (x, y) should be passed to point.
    Pygame sprite object should be passed to sprite."""
    point_x = point[0]
    point_y = point[1]

    if (sprite.rect.left <= point_x <= sprite.rect.right and
       sprite.rect.top <= point_y <= sprite.rect.bottom):
        return True
    return False
