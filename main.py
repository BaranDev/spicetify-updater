"""
Main entry point for Spicetify Updater.
This file ensures proper imports regardless of how the application is run.
"""

import sys
import os

# Ensure the src directory is in the path
if __name__ == "__main__":
    # Add the current directory to the path so imports work
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Import and run via the safe wrapper (catches all unhandled exceptions)
    from src.core.main import _safe_main

    _safe_main()

