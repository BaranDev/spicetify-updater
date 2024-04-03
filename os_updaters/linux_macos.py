import subprocess
from pathlib import Path
import requests


def install_spicetify():
    """Installs Spicetify CLI, asking the user if they want to install the Marketplace too."""
    script_dir = Path("installation-scripts")
    script_dir.mkdir(exist_ok=True)  # Ensure the directory exists
    script_path = script_dir / "install_spicetify.sh"

    # Download the install script for Spicetify
    download_cmd = f"curl -o {script_path} https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.sh"

    print("Downloading Spicetify install script...")
    subprocess.run(download_cmd, shell=True, check=True)

    run_cmd = f"sh {script_path}"

    try:
        subprocess.run(run_cmd, shell=True, check=True)
        print("Spicetify CLI installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Spicetify CLI. {str(e)}")

    try:
        subprocess.run(["spicetify", "backup"], check=True)
        subprocess.run(["sudo", "chmod", "a+wr", "/usr/share/spotify"], check=True)
        subprocess.run(
            ["sudo", "chmod", "a+wr", "/usr/share/spotify/Apps", "-R"], check=True
        )
        subprocess.run(["spicetify", "apply"], check=True)
        print("Spicetify backup applied successfully.")
    except subprocess.CalledProcessError as e:
        print(
            f"Failed to apply Spicetify backup. {str(e)}. Please try applying manually with 'spicetify apply'."
        )


def is_spicetify_installed():
    """Checks if Spicetify is installed by running the 'spicetify --version' command."""
    try:
        subprocess.run(
            ["spicetify", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except:
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
        result = subprocess.run(["spicetify", "-v"], capture_output=True, text=True)
        installed_version = result.stdout.strip()
        return installed_version
    except subprocess.CalledProcessError:
        print("Error getting Spicetify version.")
        return None


def is_spicetify_up_to_date():
    """Checks if the installed version of Spicetify is up to date."""
    installed_version = get_current_spicetify_version()
    latest_version = get_latest_spicetify_version()

    if latest_version:
        print(f"Latest version: {latest_version}")
        print(f"Current version: {installed_version}")
        return installed_version == latest_version
    else:
        print("Failed to fetch latest Spicetify version.")
        return False


# UNIT TEST
if __name__ == "__main__":
    if not is_spicetify_installed():
        print("spicetify is not installed. installing spicetify...")
        install_spicetify()
    else:
        print("spicetify is already installed.")

    if is_spicetify_up_to_date():
        print("spicetify is up to date.")
    else:
        print("spicetify is not up to date. please update manually.")

# CHECKLIST FOR TESTING THIS SCRIPT:
# Linux Distros:
#   [✔] Ubuntu (Latest LTS and the most recent release)
#   [ ] Fedora (Latest release)
#   [ ] Debian (Stable release)
#   [ ] CentOS (Latest release - Note: transitioning to CentOS Stream)
#   [ ] Arch Linux (Rolling release)
#   [ ] OpenSUSE (Leap and Tumbleweed)
# macOS Versions:
#   [ ] The latest version of macOS
