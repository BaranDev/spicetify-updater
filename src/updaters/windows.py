import subprocess
import logging
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


def _run_powershell(command, check=True):
    """Run a PowerShell command and return the result."""
    return subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=check,
    )


def _run_shell(command, check=True):
    """Run a shell command and return the result."""
    return subprocess.run(command, shell=True, capture_output=True, text=True, check=check)


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def is_spicetify_installed():
    """Check if Spicetify CLI is available on the system."""
    try:
        result = _run_shell("spicetify --version", check=False)
        # On Windows, an unrecognized command prints an error message
        if result.returncode != 0:
            return False
        if "is not recognized" in result.stdout or "is not recognized" in result.stderr:
            return False
        return bool(result.stdout.strip())
    except Exception:
        return False


def get_current_version():
    """Get the currently installed Spicetify version string."""
    try:
        result = _run_shell("spicetify -v", check=False)
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
    # If we cannot determine either version, assume not up to date
    return (False, current, latest)


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def install_spicetify():
    """Install Spicetify CLI using the official PowerShell script."""
    logger.info("Installing Spicetify CLI via PowerShell...")
    result = _run_powershell(_INSTALL_SPICETIFY_CMD, check=False)
    if result.returncode != 0:
        logger.error("Spicetify install failed: %s", result.stderr.strip())
        raise RuntimeError("Spicetify installation failed.")
    logger.info("Spicetify CLI installed.")


def install_marketplace():
    """Install the Spicetify Marketplace extension."""
    logger.info("Installing Spicetify Marketplace...")
    result = _run_powershell(_INSTALL_MARKETPLACE_CMD, check=False)
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
    result = _run_shell("spicetify upgrade", check=False)
    if result.returncode != 0:
        logger.error("Spicetify upgrade failed: %s", result.stderr.strip())
        raise RuntimeError("Spicetify upgrade failed.")

    logger.info("Re-applying Spicetify after upgrade...")
    apply_result = _run_shell("spicetify restore backup apply", check=False)
    if apply_result.returncode != 0:
        logger.warning(
            "restore backup apply returned non-zero: %s", apply_result.stderr.strip()
        )
    logger.info("Spicetify upgraded and re-applied.")


def apply_spicetify():
    """Backup and apply Spicetify (e.g. after a Spotify update)."""
    logger.info("Running spicetify backup apply...")
    result = _run_shell("spicetify backup apply", check=False)
    if result.returncode != 0:
        logger.warning("backup apply returned non-zero: %s", result.stderr.strip())
        raise RuntimeError("spicetify backup apply failed.")
    logger.info("Spicetify applied successfully.")
