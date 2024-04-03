# os_updaters/__init__.py

from .windows import (
    install_spicetify as install_spicetify_windows,
    update_spicetify as update_spicetify_windows,
)
from .linux_macos import (
    install_spicetify as install_spicetify_linux_macos,
    update_spicetify as update_spicetify_linux_macos,
)
