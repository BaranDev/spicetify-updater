import subprocess
import logging
import platform
import os
import requests

logger = logging.getLogger(__name__)

# GitHub API endpoint for latest Spicetify release
_GITHUB_API_URL = "https://api.github.com/repos/spicetify/cli/releases/latest"
_USER_AGENT = "SpicetifyUpdater/2.0"

# Official install script
_INSTALL_CMD = "curl -fsSL https://raw.githubusercontent.com/spicetify/cli/main/install.sh | sh"
_INSTALL_MARKETPLACE_CMD = (
    "curl -fsSL https://raw.githubusercontent.com/spicetify/marketplace/main/resources/install.sh | sh"
)


def _run(command, check=True):
    """Run a shell command and return the result."""
    return subprocess.run(command, shell=True, capture_output=True, text=True, check=check)


def _get_os_type():
    """Return 'macos' or 'linux'."""
    return "macos" if platform.system() == "Darwin" else "linux"


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def is_spicetify_installed():
    """Check if Spicetify CLI is available on the system."""
    try:
        result = _run("spicetify --version", check=False)
        if result.returncode != 0:
            return False
        return bool(result.stdout.strip())
    except Exception:
        return False


def get_current_version():
    """Get the currently installed Spicetify version string."""
    try:
        result = _run("spicetify -v", check=False)
        return result.stdout.strip() or None
    except Exception:
        return None


def get_latest_version():
    """Fetch the latest Spicetify version tag from GitHub."""
    try:
        response = requests.get(
            _GITHUB_API_URL,
            headers={"User-Agent": _USER_AGENT},
            timeout=10,
        )
        if response.status_code == 200:
            tag = response.json().get("tag_name", "")
            return tag.lstrip("v")
        logger.warning("GitHub API returned status %d", response.status_code)
        return None
    except requests.RequestException as exc:
        logger.warning("Failed to reach GitHub API: %s", exc)
        return None


def is_up_to_date():
    """Compare installed version against the latest GitHub release.

    Returns a tuple (up_to_date: bool, current: str | None, latest: str | None).
    """
    current = get_current_version()
    latest = get_latest_version()
    if current and latest:
        return (current == latest, current, latest)
    return (False, current, latest)


# ---------------------------------------------------------------------------
# Spotify path & permissions helpers
# ---------------------------------------------------------------------------

_LINUX_SPOTIFY_PATHS = [
    "/usr/share/spotify",
    "/opt/spotify",
    os.path.expanduser("~/.local/share/spotify-launcher/install/usr/share/spotify"),
]

_FLATPAK_SPOTIFY_PATHS = [
    "/var/lib/flatpak/app/com.spotify.Client/x86_64/stable/active/files/extra/share/spotify/",
    os.path.expanduser(
        "~/.local/share/flatpak/app/com.spotify.Client/x86_64/stable/active/files/extra/share/spotify/"
    ),
]

_PREFS_PATHS = [
    os.path.expanduser("~/.config/spotify/prefs"),
    os.path.expanduser("~/.var/app/com.spotify.Client/config/spotify/prefs"),
]


def _detect_spotify_install():
    """Detect the Spotify installation type on Linux.

    Returns one of: 'snap', 'flatpak', 'standard'.
    """
    # Check Snap
    snap_check = _run("which snap", check=False)
    if snap_check.returncode == 0:
        snap_list = _run("snap list spotify", check=False)
        if snap_list.returncode == 0:
            return "snap"

    # Check Flatpak
    flatpak_check = _run("which flatpak", check=False)
    if flatpak_check.returncode == 0:
        flatpak_list = _run("flatpak list --app", check=False)
        if "com.spotify.Client" in flatpak_list.stdout:
            return "flatpak"

    return "standard"


def _configure_spotify_path():
    """Auto-detect the Spotify path and configure Spicetify accordingly.

    macOS: Sets the standard /Applications path.
    Linux: Handles standard, Flatpak, and warns about Snap.
    """
    os_type = _get_os_type()

    if os_type == "macos":
        path = "/Applications/Spotify.app/Contents/Resources"
        logger.info("Setting Spotify path for macOS: %s", path)
        _run(f'spicetify config spotify_path "{path}"', check=False)
        return

    # Linux
    install_type = _detect_spotify_install()

    if install_type == "snap":
        logger.warning(
            "Spotify installed from Snap cannot be modified by Spicetify. "
            "Uninstall the Snap version and reinstall via apt or Flatpak."
        )
        raise RuntimeError(
            "Spotify is installed via Snap, which cannot be modified. "
            "Please reinstall Spotify using apt or Flatpak."
        )

    if install_type == "flatpak":
        # Find Spotify path
        for path in _FLATPAK_SPOTIFY_PATHS:
            if os.path.exists(path):
                logger.info("Found Flatpak Spotify at: %s", path)
                _run(f'spicetify config spotify_path "{path}"', check=False)

                # Find prefs file
                for prefs in _PREFS_PATHS:
                    if os.path.exists(prefs):
                        logger.info("Found prefs file at: %s", prefs)
                        _run(f'spicetify config prefs_path "{prefs}"', check=False)
                        break

                # Set permissions
                _run(f"sudo chmod a+wr {path}", check=False)
                _run(f"sudo chmod a+wr -R {path}/Apps", check=False)
                return

        logger.warning("Could not locate Flatpak Spotify installation.")
        return

    # Standard Linux installation
    for path in _LINUX_SPOTIFY_PATHS:
        if os.path.exists(path):
            logger.info("Found Spotify at: %s", path)
            _run(f'spicetify config spotify_path "{path}"', check=False)
            _run(f"sudo chmod a+wr {path}", check=False)
            _run(f"sudo chmod a+wr -R {path}/Apps", check=False)
            return

    logger.warning("Could not auto-detect Spotify path. You may need to set it manually.")


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def install_spicetify():
    """Install Spicetify CLI using the official shell script."""
    logger.info("Installing Spicetify CLI...")
    result = _run(_INSTALL_CMD, check=False)
    if result.returncode != 0:
        logger.error("Spicetify install failed: %s", result.stderr.strip())
        raise RuntimeError("Spicetify installation failed.")
    logger.info("Spicetify CLI installed.")

    # Configure Spotify path and permissions
    _configure_spotify_path()


def install_marketplace():
    """Install the Spicetify Marketplace extension."""
    logger.info("Installing Spicetify Marketplace...")
    result = _run(_INSTALL_MARKETPLACE_CMD, check=False)
    if result.returncode != 0:
        logger.error("Marketplace install failed: %s", result.stderr.strip())
        raise RuntimeError("Marketplace installation failed.")
    logger.info("Spicetify Marketplace installed.")


def upgrade_spicetify():
    """Upgrade Spicetify CLI to the latest version.

    Uses ``spicetify upgrade`` followed by ``spicetify restore backup apply``
    as recommended by the official documentation.
    """
    logger.info("Upgrading Spicetify CLI...")
    result = _run("spicetify upgrade", check=False)
    if result.returncode != 0:
        logger.error("Spicetify upgrade failed: %s", result.stderr.strip())
        raise RuntimeError("Spicetify upgrade failed.")

    logger.info("Re-applying Spicetify after upgrade...")
    apply_result = _run("spicetify restore backup apply", check=False)
    if apply_result.returncode != 0:
        logger.warning(
            "restore backup apply returned non-zero: %s", apply_result.stderr.strip()
        )
    logger.info("Spicetify upgraded and re-applied.")


def apply_spicetify():
    """Backup and apply Spicetify (e.g. after a Spotify update)."""
    logger.info("Running spicetify backup apply...")
    result = _run("spicetify backup apply", check=False)
    if result.returncode != 0:
        logger.warning("backup apply returned non-zero: %s", result.stderr.strip())
        raise RuntimeError("spicetify backup apply failed.")
    logger.info("Spicetify applied successfully.")
