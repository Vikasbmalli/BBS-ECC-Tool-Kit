"""Modulo Crypto Lab - run this file to start the web app.

    python app.py            # opens http://localhost:8000
    python app.py --port 9000

Uses only the Python standard library (no pip install needed).
"""
import argparse
import functools
import http.server
import os
import socketserver
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser(description="Run the Modulo web app")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-browser", action="store_true", help="do not open the browser automatically")
    args = ap.parse_args()

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as server:
        url = f"http://localhost:{args.port}/index.html#login"
        print("=" * 52)
        print(" Modulo Crypto Lab is running")
        print(f" Open this URL:  {url}")
        print(" Press Ctrl+C to stop the server")
        print("=" * 52)
        if not args.no_browser:
            threading.Timer(0.8, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
