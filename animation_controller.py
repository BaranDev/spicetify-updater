# animation_controller.py

import time
from styling import CAT_FRAMES, THUMBS_UP


def play_cool_cat_animation():
    """Play the cool cat ASCII animation."""
    for _ in range(3):  # Loop the animation 3 times
        for frame in CAT_FRAMES:
            print("\033c", end="")  # Clear the console
            print(frame)
            time.sleep(1.4)  # Wait a bit before showing the next frame


def print_thumbs_up():
    """Print the thumbs up ASCII art."""
    print("\033c", end="")  # Clear the console
    print(THUMBS_UP)


# if __name__ == "__main__":
# Uncomment for direct testing
# play_cool_cat_animation()
# print_thumbs_up()
