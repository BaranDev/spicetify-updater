# Spicetify Updater

A simple tool that installs and keeps [Spicetify](https://spicetify.app/) up to date on your computer.

## How to Use

1. Download the latest version for your system from the [Releases](https://github.com/barandev/spicetify-updater/releases) page.
2. Run it.
3. Follow the on-screen prompts.

The tool will automatically check if Spicetify is installed, install it if needed, and update it to the latest version.

## What It Handles

- Installing Spicetify and the [Marketplace](https://github.com/spicetify/marketplace) for you
- Checking for new Spicetify versions
- Upgrading and re-applying Spicetify after updates

## Supported Platforms

| Platform | Status |
|----------|--------|
| Windows 10/11 | Supported |
| Linux (apt, Flatpak) | Supported |
| macOS | Supported |
| Linux (Snap) | Not supported |

## Troubleshooting

### "Spicetify stopped working after a Spotify update"

This is normal. Spotify updates overwrite the files Spicetify modifies.

1. Run the updater again.
2. When asked to re-apply Spicetify, choose **Yes**.
3. Spotify will restart with your customizations back in place.

If the updater says Spicetify itself also needs an update, let it upgrade first.

---

### "Cannot find pref_file" (Windows)

This usually means you have the **Microsoft Store** version of Spotify, which does not work with Spicetify.

1. Open Spotify and go to **Settings > About** to check your version.
2. If it says "Microsoft Store", uninstall Spotify from Windows Settings.
3. Download and install the regular version from [spotify.com/download](https://www.spotify.com/download/).
4. Open Spotify, log in, and **wait at least 60 seconds** before closing it.
5. Run the updater again.

If you already have the regular version and still see this error:

1. Open File Explorer and go to `%appdata%\Spotify`.
2. Check if a file called `prefs` exists there.
3. If it does not exist, open Spotify, wait 60 seconds, then close it and check again.

---

### "Spicetify is not recognized" or "command not found"

The updater could not find Spicetify on your system. This can happen if Spicetify was not added to your system PATH during installation.

**Windows:**

1. Close and reopen your terminal or command prompt.
2. Try running the updater again.
3. If it still fails, restart your computer and try once more.

**Linux / macOS:**

1. Close and reopen your terminal.
2. If the issue persists, add Spicetify to your PATH manually:
   - Open your shell config file (`~/.bashrc`, `~/.zshrc`, or equivalent).
   - Add this line at the end: `export PATH=$PATH:~/.spicetify`
   - Save the file, then run `source ~/.bashrc` (or `source ~/.zshrc`).
3. Run the updater again.

---

### Spotify installed via Snap (Linux)

Snap packages are sandboxed and cannot be modified by Spicetify. You need to switch to a different installation method.

1. Remove the Snap version:
   ```
   snap remove spotify
   ```
2. Install Spotify via apt:
   ```
   curl -sS https://download.spotify.com/debian/pubkey_C85668DF69375001.gpg | sudo gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/spotify.gpg
   echo "deb http://repository.spotify.com stable non-free" | sudo tee /etc/apt/sources.list.d/spotify.list
   sudo apt-get update && sudo apt-get install spotify-client
   ```
3. Open Spotify, log in, and wait at least 60 seconds.
4. Run the updater again.

---

### The updater cannot check for updates (network error)

The updater checks GitHub for the latest Spicetify version. If this fails:

1. Make sure you have an active internet connection.
2. Try again in a few minutes (GitHub may be temporarily unavailable).
3. If you are behind a corporate firewall or VPN, try disconnecting and running the updater on a regular connection.

---

### Spicetify themes or extensions disappeared

After an upgrade, Spicetify resets its modifications to ensure compatibility with the new version.

1. Open Spotify.
2. Go to the **Marketplace** tab in the sidebar.
3. Reinstall your preferred themes and extensions from there.

Your Marketplace settings and installed items are stored locally and may reappear automatically after re-applying.

## License

[MIT](LICENSE)
