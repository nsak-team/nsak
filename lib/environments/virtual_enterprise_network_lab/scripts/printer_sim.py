import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ADMIN_HTML = b"""\
<!DOCTYPE html>
<html>
<head><title>HP LaserJet 8101</title></head>
<body>
<h1>HP LaserJet Pro 8101</h1>
<table border="1" cellpadding="4">
  <tr><td>Firmware</td> <td>FW 002.1902A</td></tr>
  <tr><td>Serial</td>   <td>CNBDF12345</td></tr>
  <tr><td>Location</td> <td>Server Room B2</td></tr>
  <tr><td>Contact</td>  <td>it@lab.local</td></tr>
  <tr><td>Pages</td>    <td>42381</td></tr>
</table>
</body>
</html>
"""

JOBS_HTML = b"""\
<!DOCTYPE html>
<html>
<head><title>IPP - Job History</title></head>
<body>
<h1>Print Job History</h1>
<table border="1" cellpadding="4">
  <tr><th>Job ID</th><th>User</th><th>Document</th><th>Status</th></tr>
  <tr><td>1042</td><td>asmith</td><td>Q3_Finance_Report.pdf</td><td>completed</td></tr>
  <tr><td>1043</td><td>bjones</td><td>network_diagram.pdf</td><td>completed</td></tr>
  <tr><td>1044</td><td>admin</td><td>server_credentials.txt</td><td>completed</td></tr>
  <tr><td>1045</td><td>asmith</td><td>payroll_oct2024.xlsx</td><td>completed</td></tr>
</table>
</body>
</html>
"""


class AdminHandler(BaseHTTPRequestHandler):
    """
    Basic admin server on /, leaks the version of the server
    """

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Server", "HP-WebServer/2.6.5")  # version leak
        self.end_headers()
        self.wfile.write(ADMIN_HTML)


class IppHandler(BaseHTTPRequestHandler):
    """
    Basic Job History server on /jobs
    """

    def do_GET(self):
        if self.path == "/jobs":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(JOBS_HTML)
        else:
            self.send_response(404)
            self.end_headers()


def serve(handler, port):
    try:
        server = ThreadingHTTPServer(("0.0.0.0", port), handler)
        print(f"[printer_sim] listening on port {port}", flush=True)
        server.serve_forever()
    except Exception as e:
        print(f"[printer_sim] FAILED on port {port}: {e}", flush=True)


for handler, port in [(AdminHandler, 80), (IppHandler, 631)]:
    threading.Thread(target=serve, args=(handler, port), daemon=True).start()

threading.Event().wait()
