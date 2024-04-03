# main.py

import platform
from subprocess import run, CalledProcessError
import sys

# Import local modules
from os_updaters import windows, linux_macos
from animation_controller import play_cool_cat_animation
from console_helper import draw_menu
from styling import show_banner


def is_spicetify_installed():
    """Checks if Spicetify is installed by trying to call it."""
    try:
        run(["spicetify", "--version"], check=True)
        return True
    except (CalledProcessError, FileNotFoundError):
        return False


def main():
    show_banner()
    # Detect operating system
    os_type = platform.system()
    if os_type not in ["Linux", "Darwin", "Windows"]:
        print("Unsupported operating system.")
        sys.exit(1)

    # Check if Spicetify is installed
    if not is_spicetify_installed():
        user_choice = input(
            "Spicetify is not installed. Would you like to install it? (y/n): "
        )
        if user_choice.lower() == "y":
            # Install Spicetify based on OS
            if os_type == "Windows":
                windows.install_spicetify()
            else:
                linux_macos.install_spicetify()
        else:
            print("Exiting...")
            sys.exit(0)
    else:
        # Spicetify is installed, check for updates or show menu
        draw_menu()


if __name__ == "__main__":
    # Uncomment the below line after implementing all components
    main()
