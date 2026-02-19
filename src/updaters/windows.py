import subprocess
import logging
import os
import requests

logger = logging.getLogger(__name__)

# GitHub API endpoint for latest Spicetify release
_GITHUB_API_URL = "https://api.github.com/repos/spicetify/cli/releases/latest"
_USER_AGENT = "SpicetifyUpdater/2.0"

# Official install scripts
_INSTALL_SPICETIFY_CMD = (
    "iwr -useb https://raw.githubusercontent.com/spicetify/cli/main/install.ps1 | iex"
)
_INSTALL_MARKETPLACE_CMD = (
    "iwr -useb https://raw.githubusercontent.com/spicetify/marketplace/main/resources/install.ps1 | iex"
)

# Known Spotify paths on Windows
_SPOTIFY_PATHS = [
    os.path.join(os.environ.get("APPDATA", ""), "Spotify"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Spotify"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WindowsApps"),
]

_MS_STORE_INDICATOR = os.path.join(
    os.environ.get("LOCALAPPDATA", ""),
    "Packages",
    "SpotifyAB.SpotifyMusic_zpdnekdrzrea0",
)

_PREFS_PATH = os.path.join(os.environ.get("APPDATA", ""), "Spotify", "prefs")


# ---------------------------------------------------------------------------
# Shell helpers
# ---------------------------------------------------------------------------

def _run_powershell(command, check=True):
    """Run a PowerShell command and return the result."""
    try:
        return subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            check=check,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "PowerShell was not found on this system. "
            "Please make sure PowerShell is installed and available in your PATH."
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to run PowerShell command: {exc}")


def _run_shell(command, check=True):
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


# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

def is_spotify_installed():
    """Check if Spotify is installed on this Windows system."""
    # Check standard install path
    appdata_spotify = os.path.join(os.environ.get("APPDATA", ""), "Spotify", "Spotify.exe")
    if os.path.isfile(appdata_spotify):
        return True

    # Check if spotify is accessible from PATH
    result = _run_shell("where spotify", check=False)
    if result.returncode == 0 and result.stdout.strip():
        return True

    return False


def is_microsoft_store_spotify():
    """Detect if the installed Spotify is the Microsoft Store version.

    The MS Store version cannot be modified by Spicetify.
    """
    return os.path.isdir(_MS_STORE_INDICATOR)


def has_spotify_prefs():
    """Check if Spotify's prefs file exists.

    The prefs file is generated after Spotify is opened and logged into for
    at least ~60 seconds. Without it, Spicetify cannot function.
    """
    return os.path.isfile(_PREFS_PATH)


def verify_prerequisites():
    """Run all pre-flight checks before install/upgrade.

    Returns a list of (level, message) tuples. Level is 'error' or 'warning'.
    An empty list means all checks passed.
    """
    issues = []

    if not is_spotify_installed():
        issues.append((
            "error",
            "Spotify does not appear to be installed.\n"
            "    Download it from https://www.spotify.com/download/ and install it first."
        ))
        return issues  # No point checking further

    if is_microsoft_store_spotify():
        issues.append((
            "error",
            "You have the Microsoft Store version of Spotify, which cannot be modified.\n"
            "    Uninstall it from Windows Settings, then download the regular version\n"
            "    from https://www.spotify.com/download/"
        ))
        return issues

    if not has_spotify_prefs():
        issues.append((
            "warning",
            "Spotify's prefs file was not found at:\n"
            f"    {_PREFS_PATH}\n"
            "    Open Spotify, log in, and wait at least 60 seconds before continuing."
        ))

    return issues


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def is_spicetify_installed():
    """Check if Spicetify CLI is available on the system."""
    try:
        result = _run_shell("spicetify --version", check=False)
        if result.returncode != 0:
            return False
        if "is not recognized" in result.stdout or "is not recognized" in result.stderr:
            return False
        return bool(result.stdout.strip())
    except (RuntimeError, Exception):
        return False


def get_current_version():
    """Get the currently installed Spicetify version string."""
    try:
        result = _run_shell("spicetify -v", check=False)
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
# Actions
# ---------------------------------------------------------------------------

def install_spicetify():
    """Install Spicetify CLI using the official PowerShell script."""
    logger.info("Installing Spicetify CLI via PowerShell...")
    result = _run_powershell(_INSTALL_SPICETIFY_CMD, check=False)
    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else "Unknown error"
        logger.error("Spicetify install failed: %s", stderr)
        raise RuntimeError(f"Spicetify installation failed: {stderr}")
    logger.info("Spicetify CLI installed.")


def install_marketplace():
    """Install the Spicetify Marketplace extension."""
    logger.info("Installing Spicetify Marketplace...")
    result = _run_powershell(_INSTALL_MARKETPLACE_CMD, check=False)
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
            "    (Scoop, Winget, Chocolatey), use that package manager to update instead."
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
