import subprocess
import requests
from pathlib import Path
import platform


def install_spicetify():
    """Installs Spicetify CLI, asking the user if they want to install the Marketplace too."""
    script_dir = Path("installation-scripts")
    script_dir.mkdir(exist_ok=True)  # Ensure the directory exists
    script_path = script_dir / "install_spicetify.ps1"

    # Download the install script for Spicetify
    download_cmd = f"Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1' -OutFile '{script_path}'"

    # Ask the user if they want to install the Marketplace too
    marketplace_install = (
        input("Do you want to install the Marketplace too? (Y/N): ").strip().lower()
    )

    # Prepare the command to run the script, assuming we can pass the choice as an argument or echo it into the input
    # Adjust the command based on how the script expects to receive the input
    if marketplace_install in ["y", "yes"]:
        marketplace_install = "echo Y |"
    else:
        marketplace_install = "echo N |"

    run_cmd = f"{marketplace_install} powershell -Command {script_path}"

    try:
        subprocess.run(["powershell", "-Command", download_cmd], check=True)
        subprocess.run(run_cmd, shell=True, check=True)
        print("Spicetify CLI installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Spicetify CLI. {str(e)}")


def is_spicetify_installed():
    """Checks if Spicetify is installed by running the 'spicetify' command."""
    try:
        result = subprocess.run(
            ["spicetify --version"], capture_output=True, text=True, shell=True
        )
        output = result.stdout.strip()
        installed = "is not recognized as an internal or external command" in output
        return not installed
    except subprocess.CalledProcessError:
        return False


def get_latest_spicetify_version():
    """Fetches the latest Spicetify version from GitHub."""
    url = "https://api.github.com/repos/spicetify/spicetify-cli/releases/latest"
    headers = {"User-Agent": "SpicetifyUpdater"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["tag_name"].strip("v")
    else:
        return None


def get_current_spicetify_version():
    """Gets the current installed version of Spicetify."""
    try:
        result = subprocess.run(
            ["spicetify", "-v"], capture_output=True, text=True, shell=True
        )
        installed_version = result.stdout.strip()
        return installed_version
    except subprocess.CalledProcessError:
        print("Error getting Spicetify version.")
        return None


def is_spicetify_up_to_date():
    """Checks if the installed version of Spicetify is up to date."""
    try:
        installed_version = get_current_spicetify_version()
        latest_version = get_latest_spicetify_version()

        if latest_version:
            print(f"Latest version: {latest_version}")
            print(f"Current version: {installed_version}")
            return installed_version == latest_version
        else:
            print("Failed to fetch latest Spicetify version.")
            return False
    except subprocess.CalledProcessError:
        print("Error checking Spicetify version.")
        return False


# UNIT TEST
# if __name__ == "__main__":
#     # Test is_spicetify_installed()
#     if is_spicetify_installed():
#         print("Spicetify is installed.")
#     else:
#         print("Spicetify is not installed.")

#     # Test get_latest_spicetify_version()
#     latest_version = get_latest_spicetify_version()
#     current_version = get_current_spicetify_version()
#     if latest_version and current_version:
#         print(f"Latest Spicetify version: {latest_version}")
#         print(f"Current Spicetify version: {current_version}")
#     else:
#         print("Failed to fetch latest Spicetify version.")

#     # Test install_marketplace()
#     install_spicetify()

# CHECKLIST FOR TESTING THIS SCRIPT:
# Windows Versions:
#   [ ] Windows 11
#   [✔] Windows 10
#   [ ] Windows 8.1
#   [ ] Windows 7
