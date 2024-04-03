import time
from styling import CAT_FRAMES, THUMBS_UP
import keyboard
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

# Initialize Pygame mixer
pygame.mixer.init()


def play_cool_cat_animation():
    # Load the background music
    pygame.mixer.music.load("resources/littleroottown.wav")
    # Play the music
    pygame.mixer.music.play(-1)  # The -1 argument makes the music loop indefinitely

    print("Press Enter to exit...")
    for frame in CAT_FRAMES:
        if keyboard.is_pressed("enter"):  # Check if Enter key has been pressed
            break  # Exit the loop if Enter is pressed
        print("\033c", end="")  # Clear the console
        print(frame)
        print("\n\t    Press Enter to exit...")  # Reminder for the user
        time.sleep(1.4)  # Wait a bit before showing the next frame

    pygame.mixer.music.stop()  # Stop the music when exiting the function
    print("\033c", end="")  # Optionally clear the console after the animation is done


if __name__ == "__main__":
    try:
        play_cool_cat_animation()
    except KeyboardInterrupt:
        pass  # Handle the case where the script is interrupted with a keyboard interrupt
    finally:
        pygame.mixer.music.stop()  # Ensure the music is stopped even if an exception occurs


def print_thumbs_up():
    """Print the thumbs up ASCII art."""
    print("\033c", end="")  # Clear the console
    print(THUMBS_UP)


# if __name__ == "__main__":
# Uncomment for direct testing
# play_cool_cat_animation()
# print_thumbs_up()
