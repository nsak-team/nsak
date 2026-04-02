#!/usr/bin/env python3
"""
mail_server.py — Realistic SMTP (Postfix 3.8) + IMAP (Dovecot 2.3) banner simulator.

Ports:
  25   SMTP  — EHLO, VRFY (user enumeration enabled), STARTTLS offered
  587  SMTP Submission — same as 25
  143  IMAP  — Dovecot banner, CAPABILITY, ID command

Recon findings this enables:
  - SMTP banner reveals: mail.lab.local, Postfix version, Ubuntu OS hint
  - EHLO reveals: PIPELINING, VRFY, STARTTLS, SIZE 52428800
  - VRFY jsmith → 250 jsmith@lab.local  (user enumeration)
  - VRFY admin  → 250 admin@lab.local
  - IMAP ID reveals: Dovecot 2.3.21, Linux 5.15
"""
import socket
import threading
import time

VALID_USERS = {
    "jsmith":      "jsmith@lab.local",
    "bjones":      "bjones@lab.local",
    "mwilson":     "mwilson@lab.local",
    "dtaylor":     "dtaylor@lab.local",
    "admin":       "admin@lab.local",
    "postmaster":  "postmaster@lab.local",
    "helpdesk":    "helpdesk@lab.local",
    "security":    "security@lab.local",
    "svc_backup":  "svc_backup@lab.local",
    "svc_web":     "svc_web@lab.local",
    "info":        "info@acmecorp.lab.local",
    "support":     "support@lab.local",
    "abuse":       "abuse@lab.local",
}


def handle_smtp(conn: socket.socket, addr: tuple) -> None:
    """SMTP handler — Postfix 3.8.x on Ubuntu banner."""
    try:
        conn.sendall(b"220 mail.lab.local ESMTP Postfix (Ubuntu)\r\n")
        while True:
            data = conn.recv(1024).decode(errors="ignore").strip()
            if not data:
                break
            upper = data.upper()
            cmd = upper.split()[0] if data.split() else ""

            if cmd in ("EHLO", "HELO"):
                conn.sendall(
                    b"250-mail.lab.local\r\n"
                    b"250-PIPELINING\r\n"
                    b"250-SIZE 52428800\r\n"
                    b"250-VRFY\r\n"
                    b"250-ETRN\r\n"
                    b"250-STARTTLS\r\n"
                    b"250-ENHANCEDSTATUSCODES\r\n"
                    b"250-8BITMIME\r\n"
                    b"250-DSN\r\n"
                    b"250 SMTPUTF8\r\n"
                )

            elif cmd == "VRFY":
                # User enumeration intentionally enabled
                arg = data[5:].strip().lower().strip("<>").split("@")[0]
                if arg in VALID_USERS:
                    conn.sendall(f"250 {VALID_USERS[arg]}\r\n".encode())
                else:
                    conn.sendall(b"550 5.1.1 <" + arg.encode() + b">: Recipient address rejected: User unknown in local recipient table\r\n")

            elif cmd == "EXPN":
                conn.sendall(b"550 5.7.1 EXPN access denied\r\n")

            elif cmd == "STARTTLS":
                conn.sendall(b"220 2.0.0 Ready to start TLS\r\n")
                # Don't actually upgrade — just send banner
                break

            elif cmd == "MAIL":
                conn.sendall(b"250 2.1.0 Ok\r\n")

            elif cmd == "RCPT":
                conn.sendall(b"250 2.1.5 Ok\r\n")

            elif cmd == "DATA":
                conn.sendall(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                # Consume data until dot
                buf = b""
                while b"\r\n.\r\n" not in buf:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    buf += chunk
                conn.sendall(b"250 2.0.0 Ok: queued as A1B2C3D4E5F6\r\n")

            elif cmd == "NOOP":
                conn.sendall(b"250 2.0.0 Ok\r\n")

            elif cmd == "RSET":
                conn.sendall(b"250 2.0.0 Ok\r\n")

            elif cmd == "QUIT":
                conn.sendall(b"221 2.0.0 Bye\r\n")
                break

            else:
                conn.sendall(b"502 5.5.2 Error: command not recognized\r\n")

    except (BrokenPipeError, ConnectionResetError):
        pass
    finally:
        conn.close()


def handle_imap(conn: socket.socket, addr: tuple) -> None:
    """IMAP handler — Dovecot 2.3.21 banner."""
    try:
        conn.sendall(
            b"* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS "
            b"ID ENABLE IDLE AUTH=PLAIN AUTH=LOGIN] Dovecot ready.\r\n"
        )
        while True:
            data = conn.recv(1024).decode(errors="ignore").strip()
            if not data:
                break
            parts = data.split(None, 2)
            if len(parts) < 2:
                continue
            tag, cmd = parts[0].encode(), parts[1].upper()
            rest = parts[2] if len(parts) > 2 else ""

            if cmd == "CAPABILITY":
                conn.sendall(
                    b"* CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS "
                    b"ID ENABLE IDLE AUTH=PLAIN AUTH=LOGIN\r\n"
                )
                conn.sendall(tag + b" OK Pre-login capabilities listed.\r\n")

            elif cmd == "ID":
                conn.sendall(
                    b'* ID ("name" "Dovecot" "version" "2.3.21" '
                    b'"os" "Linux" "os-version" "5.15.0-101-generic" '
                    b'"support-url" "https://www.dovecot.org/" '
                    b'"support-email" "dovecot@dovecot.org")\r\n'
                )
                conn.sendall(tag + b" OK ID completed.\r\n")

            elif cmd == "LOGIN":
                # Always reject — not a real auth server
                conn.sendall(tag + b" NO [AUTHENTICATIONFAILED] Authentication failed.\r\n")

            elif cmd == "AUTHENTICATE":
                conn.sendall(b"+ \r\n")
                conn.recv(1024)  # consume credentials
                conn.sendall(tag + b" NO [AUTHENTICATIONFAILED] Authentication failed.\r\n")

            elif cmd == "LOGOUT":
                conn.sendall(b"* BYE Logging out\r\n")
                conn.sendall(tag + b" OK Logout completed.\r\n")
                break

            elif cmd == "NOOP":
                conn.sendall(tag + b" OK NOOP completed.\r\n")

            else:
                conn.sendall(tag + b" BAD Error in IMAP command received by server.\r\n")

    except (BrokenPipeError, ConnectionResetError):
        pass
    finally:
        conn.close()


def serve(port: int, handler) -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", port))
    srv.listen(20)
    print(f"[mail] Listening on :{port}", flush=True)
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handler, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    for port, handler in [
        (25,  handle_smtp),
        (587, handle_smtp),
        (143, handle_imap),
    ]:
        threading.Thread(target=serve, args=(port, handler), daemon=True).start()

    while True:
        time.sleep(60)
