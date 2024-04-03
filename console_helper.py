def display_welcome_message():
    print("Welcome to the Spicetify Updater!")
    # Additional welcome message content
    # You can use styling from styling.py here


def request_user_action():
    action = input("Update complete. Press any key to exit or 'a' for animations: ")
    if action.lower() == "a":
        from animation_controller import start_ascii_animation

        start_ascii_animation()
    else:
        print("Exiting...")
