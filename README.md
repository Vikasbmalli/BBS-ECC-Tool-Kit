# Modulo Crypto Lab

BCS703 Module 2 project: Blum Blum Shub (PRNG) and Elliptic Curve Cryptography (ECDH + AES-GCM) with a full web interface.

## Run the web app (Python)
    python app.py

This starts a local server and opens http://localhost:8000/index.html#login in your browser. Press Ctrl+C in the terminal to stop it.
Use `python app.py --port 9000` if port 8000 is busy. No pip install is needed for this step.

You can also just double-click `index.html`; it works without the server.
The page loads its fonts from Google Fonts when online and falls back to system fonts offline.

Both experiments have a **Step by step** mode: choose it at the top of the Inputs panel, press Start, then press **Next step** to run one calculation at a time (Back, Show all and Restart are also there; the left and right arrow keys work too).

Pages: Login, Register, Dashboard, Blum Blum Shub, ECC + AES-GCM, Learn, Profile.
Use "Try the demo account" on the login page, or register your own account.

Accounts are kept in the browser's localStorage and passwords are salted and hashed (SHA-256).
This is a classroom demo and not a substitute for real authentication.

## Folder contents
- `app.py`          starts the web app at http://localhost:8000
- `index.html`      the whole web app (HTML, CSS and JavaScript in one file)
- `assets/backgrounds/`  the five background images used by the pages (PNG, 1920x1080). The app draws them live in the browser, these are copies for reports and slides.
- `screenshots/`    screenshots of every page
- `logo.svg`        project logo
- `bbs.py`, `ecc_demo.py`, `requirements.txt`   the original command-line versions
- `PROJECT_NOTES.txt`  algorithm notes

## Run the command-line versions
    pip install -r requirements.txt
    python bbs.py
    python ecc_demo.py

## Viva summary
- BBS: squares the state modulo n = p*q and outputs the lowest bit of each new state.
- ECDH: Alice and Bob exchange public points on P-256 and each derive the same shared secret.
- HKDF-SHA256 turns that secret into an AES key; AES-GCM encrypts and authenticates the message.
