#!/usr/bin/env python3
"""
Simple HTTP server to serve the Sanga Portal frontend.
Run this script to start the frontend server on port 3000.
"""

import http.server
import socketserver
import os
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Set the directory to serve files from
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_server(port=3000):
    """Run the HTTP server"""
    # Change to frontend directory
    frontend_dir = Path(__file__).parent / 'frontend'
    os.chdir(frontend_dir)

    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        print(f"Serving Sanga Portal frontend at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()