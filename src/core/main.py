"""
Spicetify Updater - main application logic.

Flow:
  1. Detect OS and load the appropriate updater module.
  2. Check if Spicetify is installed; offer to install if not.
  3. Check for updates via the GitHub API.
  4. Upgrade or re-apply as needed.
"""

import platform
import logging
import sys
import os

# Configure logging once at the top level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("spicetify-updater.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# OS detection and dynamic import
# ---------------------------------------------------------------------------

_SYSTEM = platform.system()

if _SYSTEM == "Windows":
    from src.updaters import windows as updater
elif _SYSTEM in ("Linux", "Darwin"):
    from src.updaters import linux_macos as updater
else:
    from src.ui.console_helper import print_error, press_enter_to_exit

    print_error(f"Unsupported operating system: {_SYSTEM}")
    press_enter_to_exit(1)

from src.ui.console_helper import (
    print_header,
    print_status,
    print_success,
    print_error,
    print_warning,
    ask_yes_no,
    press_enter_to_exit,
)


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------


def main():
    print_header()

    # --- Step 1: Is Spicetify installed? ---
    print_status("Checking if Spicetify is installed...")

    if not updater.is_spicetify_installed():
        print_warning("Spicetify is not installed on this system.")
        if ask_yes_no("Would you like to install Spicetify?"):
            try:
                updater.install_spicetify()
                print_success("Spicetify installed.")
            except RuntimeError as exc:
                print_error(str(exc))
                press_enter_to_exit(1)

            # Offer to install Marketplace
            if ask_yes_no("Install the Spicetify Marketplace too? (Recommended)"):
                try:
                    updater.install_marketplace()
                    print_success("Marketplace installed.")
                except RuntimeError as exc:
                    print_warning(f"Marketplace install issue: {exc}")

            # First-time setup: backup and apply
            print_status("Applying Spicetify for the first time...")
            try:
                updater.apply_spicetify()
                print_success("Spicetify applied to Spotify.")
            except RuntimeError as exc:
                print_warning(f"Apply issue: {exc}")

            print_success("All done!")
            press_enter_to_exit(0)
        else:
            print_status("Installation skipped.")
            press_enter_to_exit(0)

    # --- Step 2: Check for updates ---
    print_success("Spicetify is installed.")
    print_status("Checking for updates...")

    up_to_date, current, latest = updater.is_up_to_date()

    if current:
        print_status(f"Installed version: {current}")
    if latest:
        print_status(f"Latest version:    {latest}")

    if up_to_date:
        print_success("Spicetify is already up to date.")

        if ask_yes_no("Re-apply Spicetify to Spotify? (Useful after a Spotify update)", default_yes=False):
            try:
                updater.apply_spicetify()
                print_success("Spicetify re-applied successfully.")
            except RuntimeError as exc:
                print_error(str(exc))
                press_enter_to_exit(1)
    else:
        if latest:
            print_warning(f"An update is available: {current} -> {latest}")
        else:
            print_warning("Could not determine the latest version. Attempting upgrade anyway.")

        if ask_yes_no("Would you like to upgrade Spicetify?"):
            try:
                updater.upgrade_spicetify()
                print_success("Spicetify upgraded and re-applied.")
            except RuntimeError as exc:
                print_error(str(exc))
                press_enter_to_exit(1)
        else:
            print_status("Upgrade skipped.")

    print_success("All done!")
    press_enter_to_exit(0)


if __name__ == "__main__":
    main()
