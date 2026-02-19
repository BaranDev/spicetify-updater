import subprocess
import logging
import platform
import os
import requests

logger = logging.getLogger(__name__)

# GitHub API endpoint for latest Spicetify release
_GITHUB_API_URL = "https://api.github.com/repos/spicetify/cli/releases/latest"
_USER_AGENT = "SpicetifyUpdater/2.0"

# Official install scripts
_INSTALL_CMD = "curl -fsSL https://raw.githubusercontent.com/spicetify/cli/main/install.sh | sh"
_INSTALL_MARKETPLACE_CMD = (
    "curl -fsSL https://raw.githubusercontent.com/spicetify/marketplace/main/resources/install.sh | sh"
)

# Known Spotify paths
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

_MACOS_SPOTIFY_PATH = "/Applications/Spotify.app"

_PREFS_PATHS = [
    os.path.expanduser("~/.config/spotify/prefs"),
    os.path.expanduser("~/.var/app/com.spotify.Client/config/spotify/prefs"),
]


# ---------------------------------------------------------------------------
# Shell helpers
# ---------------------------------------------------------------------------

def _run(command, check=True):
    """Run a shell command and return the result (output captured)."""
    try:
        return subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
    except OSError as exc:
        raise RuntimeError(f"Failed to run command '{command}': {exc}")


def _run_live(command):
    """Run a shell command, capturing output into the log file.

    The raw output is hidden from the user to keep the terminal clean.
    """
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )
        if result.stdout:
            logger.debug("stdout: %s", result.stdout.strip())
        if result.stderr:
            logger.debug("stderr: %s", result.stderr.strip())
        return result
    except OSError as exc:
        raise RuntimeError(f"Failed to run command '{command}': {exc}")


def _get_os_type():
    """Return 'macos' or 'linux'."""
    return "macos" if platform.system() == "Darwin" else "linux"


# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

def is_spotify_installed():
    """Check if Spotify is installed on this system."""
    os_type = _get_os_type()

    if os_type == "macos":
        return os.path.isdir(_MACOS_SPOTIFY_PATH)

    # Linux: check standard paths
    for path in _LINUX_SPOTIFY_PATHS:
        if os.path.isdir(path):
            return True

    # Check Flatpak paths
    for path in _FLATPAK_SPOTIFY_PATHS:
        if os.path.isdir(path):
            return True

    # Check if spotify is in PATH
    result = _run("which spotify", check=False)
    if result.returncode == 0 and result.stdout.strip():
        return True

    # Check Flatpak list
    result = _run("flatpak list --app 2>/dev/null", check=False)
    if "com.spotify.Client" in (result.stdout or ""):
        return True

    return False


def _is_snap_spotify():
    """Check if Spotify is installed via Snap."""
    result = _run("which snap", check=False)
    if result.returncode != 0:
        return False
    snap_list = _run("snap list spotify 2>/dev/null", check=False)
    return snap_list.returncode == 0


def has_spotify_prefs():
    """Check if Spotify's prefs file exists.

    The prefs file is generated after Spotify is opened and logged into for
    at least ~60 seconds. Without it, Spicetify cannot function.
    """
    for path in _PREFS_PATHS:
        if os.path.isfile(path):
            return True
    return False


def verify_prerequisites():
    """Run all pre-flight checks before install/upgrade.

    Returns a list of (level, message) tuples. Level is 'error' or 'warning'.
    An empty list means all checks passed.
    """
    issues = []
    os_type = _get_os_type()

    if not is_spotify_installed():
        if os_type == "macos":
            issues.append((
                "error",
                "Spotify does not appear to be installed.\n"
                "    Download it from https://www.spotify.com/download/ and install it first."
            ))
        else:
            issues.append((
                "error",
                "Spotify does not appear to be installed.\n"
                "    Install it via your package manager (apt, Flatpak) or from\n"
                "    https://www.spotify.com/download/"
            ))
        return issues

    if os_type == "linux" and _is_snap_spotify():
        issues.append((
            "error",
            "Spotify is installed via Snap, which cannot be modified by Spicetify.\n"
            "    Uninstall the Snap version (snap remove spotify) and reinstall via\n"
            "    apt or Flatpak. See the README for step-by-step instructions."
        ))
        return issues

    if not has_spotify_prefs():
        issues.append((
            "warning",
            "Spotify's prefs file was not found.\n"
            "    Open Spotify, log in, and wait at least 60 seconds before continuing.\n"
            "    Checked paths: " + ", ".join(_PREFS_PATHS)
        ))

    return issues


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
    except (RuntimeError, Exception):
        return False


def get_current_version():
    """Get the currently installed Spicetify version string."""
    try:
        result = _run("spicetify -v", check=False)
        return result.stdout.strip() or None
    except (RuntimeError, Exception):
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

    # Linux - Snap is already blocked by verify_prerequisites()

    # Check Flatpak
    for path in _FLATPAK_SPOTIFY_PATHS:
        if os.path.exists(path):
            logger.info("Found Flatpak Spotify at: %s", path)
            _run(f'spicetify config spotify_path "{path}"', check=False)

            for prefs in _PREFS_PATHS:
                if os.path.exists(prefs):
                    logger.info("Found prefs file at: %s", prefs)
                    _run(f'spicetify config prefs_path "{prefs}"', check=False)
                    break

            _run(f"sudo chmod a+wr {path}", check=False)
            _run(f"sudo chmod a+wr -R {path}/Apps", check=False)
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

    # Verify curl is available
    curl_check = _run("which curl", check=False)
    if curl_check.returncode != 0:
        raise RuntimeError(
            "curl is required to install Spicetify but was not found.\n"
            "    Install it with your package manager (e.g. sudo apt install curl)."
        )

    result = _run(_INSTALL_CMD, check=False)
    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else "Unknown error"
        logger.error("Spicetify install failed: %s", stderr)
        raise RuntimeError(f"Spicetify installation failed: {stderr}")
    logger.info("Spicetify CLI installed.")

    # Configure Spotify path and permissions
    _configure_spotify_path()


def install_marketplace():
    """Install the Spicetify Marketplace extension."""
    logger.info("Installing Spicetify Marketplace...")
    result = _run(_INSTALL_MARKETPLACE_CMD, check=False)
    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else "Unknown error"
        logger.error("Marketplace install failed: %s", stderr)
        raise RuntimeError(f"Marketplace installation failed: {stderr}")
    logger.info("Spicetify Marketplace installed.")


def upgrade_spicetify():
    """Upgrade Spicetify CLI to the latest version.

    Uses ``spicetify upgrade`` followed by ``spicetify restore backup apply``
    as recommended by the official documentation.
    """
    logger.info("Upgrading Spicetify CLI...")
    result = _run_live("spicetify upgrade")
    if result.returncode != 0:
        raise RuntimeError(
            "Spicetify upgrade failed. If you installed Spicetify via a package manager\n"
            "    (Homebrew, AUR), use that package manager to update instead."
        )

    logger.info("Re-applying Spicetify after upgrade...")
    _run_live("spicetify restore")
    _run_live("spicetify backup")  # non-zero is OK (backup already exists)
    result = _run_live("spicetify apply")
    if result.returncode != 0:
        raise RuntimeError(
            "spicetify apply failed after upgrade.\n"
            "    Try closing Spotify completely and running this tool again."
        )
    logger.info("Spicetify upgraded and re-applied.")


def apply_spicetify():
    """Backup and apply Spicetify (e.g. after a Spotify update)."""
    logger.info("Backing up Spotify...")
    _run_live("spicetify backup")  # non-zero is OK (backup already exists)

    logger.info("Applying Spicetify...")
    result = _run_live("spicetify apply")
    if result.returncode != 0:
        raise RuntimeError(
            "spicetify apply failed.\n"
            "    Try closing Spotify completely and running this tool again.\n"
            "    If the problem persists, run: spicetify restore backup apply"
        )
    logger.info("Spicetify applied successfully.")
