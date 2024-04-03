import platform
from animation_controller import play_cool_cat_animation
from console_helper import display_menu

# Conditional import based on the OS
if platform.system() == "Windows":
    from os_updaters import windows as os_updater
else:
    from os_updaters import linux_macos as os_updater

SPICETIFY_INSTALLED = os_updater.is_spicetify_installed()
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


def main():
    if not SPICETIFY_INSTALLED:
        user_choice = input(
            "Spicetify is not installed. Would you like to install it? (Y/N): "
        ).lower()
        if user_choice == "y":
            os_updater.install_spicetify()
            print("Spicetify has been installed.")
        else:
            print("Spicetify installation skipped.")
            return  # Exit the program if Spicetify isn't installed and the user chooses not to install it.

    # Now check if Spicetify is up to date.
    if not os_updater.is_spicetify_up_to_date():
        user_choice = input(
            "An update for Spicetify is available. Would you like to update? (Y/N): "
        ).lower()
        if user_choice == "y":
            os_updater.update_spicetify()
            print("Spicetify has been updated.")
        else:
            print("Spicetify update skipped.")

    # Main menu
    while True:
        if SPICETIFY_INSTALLED:
            options = ["Reinstall/Update Spicetify", "See a cool cat animation"]
            user_choice = display_menu(options)
            if user_choice == "1":
                os_updater.install_spicetify()
            elif user_choice == "2":
                play_cool_cat_animation()
            elif user_choice == "3":
                print("Exiting...")
                break  # Exit the while loop to terminate the program
            else:
                print("Invalid option. Please try again.")
        else:
            options = ["Install Spicetify", "See a cool cat animation"]
            user_choice = display_menu(options)
            if user_choice == "1":
                os_updater.install_spicetify()
            elif user_choice == "2":
                play_cool_cat_animation()
            elif user_choice == "3":
                print("Exiting...")
                break


if __name__ == "__main__":
    main()
