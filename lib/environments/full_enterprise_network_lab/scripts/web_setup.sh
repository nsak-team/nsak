#!/bin/sh
# web_setup.sh — nginx config + TLS cert + realistic web content for recon training

set -e

mkdir -p /etc/nginx/ssl /srv/www/acme

# ── Self-signed TLS certificate (recon artifact: cert reveals org/SAN) ────────
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/server.key \
  -out    /etc/nginx/ssl/server.crt \
  -subj   "/C=CH/ST=Bern/L=Bern/O=Acme Corp AG/OU=IT Operations/CN=web.lab.local" \
  -addext "subjectAltName=DNS:web.lab.local,DNS:acmecorp.lab.local,DNS:www.lab.local,IP:172.16.1.10" \
  2>/dev/null

# ── Remove default nginx vhost ────────────────────────────────────────────────
rm -f /etc/nginx/conf.d/default.conf

# ── nginx vhost config ────────────────────────────────────────────────────────
cat > /etc/nginx/conf.d/acme.conf << 'EOF'
server {
    listen 80;
    server_name web.lab.local acmecorp.lab.local www.lab.local;
    root /srv/www/acme;
    index index.html;

    add_header Server "nginx/1.25.3";
    add_header X-Powered-By "PHP/8.2.7";
    add_header X-Frame-Options "SAMEORIGIN";

    # robots.txt — intentionally reveals interesting paths
    location = /robots.txt {
        add_header Content-Type text/plain;
        return 200 "User-agent: *\nDisallow: /admin\nDisallow: /backup\nDisallow: /api/internal\nDisallow: /dev\nDisallow: /.git\n";
    }

    # Fake API endpoint — reveals version info
    location /api/v1/status {
        add_header Content-Type application/json;
        return 200 '{"status":"ok","version":"1.3.2","env":"production","db_host":"db.lab.local","domain":"lab.local"}';
    }

    location /admin    { return 401 "Unauthorized"; }
    location /backup   { return 403 "Forbidden"; }
    location /dev      { return 403 "Forbidden"; }

    location / { try_files $uri $uri/ =404; }
}

server {
    listen 443 ssl;
    server_name web.lab.local acmecorp.lab.local www.lab.local;
    root /srv/www/acme;
    index index.html;

    ssl_certificate     /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    ssl_protocols       TLSv1.2 TLSv1.3;

    add_header Server "nginx/1.25.3";
    add_header X-Powered-By "PHP/8.2.7";

    location = /robots.txt {
        add_header Content-Type text/plain;
        return 200 "User-agent: *\nDisallow: /admin\nDisallow: /backup\nDisallow: /api/internal\nDisallow: /dev\nDisallow: /.git\n";
    }

    location /api/v1/status {
        add_header Content-Type application/json;
        return 200 '{"status":"ok","version":"1.3.2","env":"production","db_host":"db.lab.local","domain":"lab.local"}';
    }

    location /admin    { return 401 "Unauthorized"; }
    location /backup   { return 403 "Forbidden"; }

    location / { try_files $uri $uri/ =404; }
}
EOF

# ── Website content ────────────────────────────────────────────────────────────
cat > /srv/www/acme/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Acme Corp AG — Enterprise Solutions</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f4f6f9; }
    header { background: #1a2e4a; color: white; padding: 20px 40px; }
    header h1 { margin: 0; font-size: 1.8em; }
    header p  { margin: 4px 0 0; color: #adc; font-size: 0.9em; }
    nav { background: #2c3e50; padding: 10px 40px; }
    nav a { color: #ecf0f1; text-decoration: none; margin-right: 20px; font-size: 0.95em; }
    nav a:hover { color: #3498db; }
    main { max-width: 900px; margin: 40px auto; padding: 0 20px; }
    .card { background: white; border-radius: 6px; padding: 24px; margin-bottom: 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,.1); }
    footer { background: #1a2e4a; color: #aaa; text-align: center;
             padding: 16px; font-size: 0.85em; margin-top: 40px; }
  </style>
</head>
<body>
  <header>
    <h1>Acme Corp AG</h1>
    <p>Enterprise IT Solutions &amp; Managed Services since 1998</p>
  </header>
  <nav>
    <a href="/">Home</a>
    <a href="/about.html">About</a>
    <a href="/services.html">Services</a>
    <a href="/contact.html">Contact</a>
    <a href="/portal.html">Employee Portal</a>
  </nav>
  <main>
    <div class="card">
      <h2>Welcome to Acme Corp AG</h2>
      <p>We provide enterprise-grade IT infrastructure, managed security services,
         and cloud migration consulting to mid-sized businesses across Europe.</p>
    </div>
    <div class="card">
      <h3>News</h3>
      <ul>
        <li>2024-03-01 — New office in Zurich opened</li>
        <li>2024-02-14 — ISO 27001 certification renewed</li>
        <li>2024-01-08 — Q4 2023 results published on intranet</li>
      </ul>
    </div>
    <div class="card">
      <h3>Contact</h3>
      <p>Email: <a href="mailto:info@acmecorp.lab.local">info@acmecorp.lab.local</a><br>
         Phone: +41 31 555 0100<br>
         IT Helpdesk: helpdesk@lab.local | Ext. 1337</p>
    </div>
  </main>
  <footer>
    &copy; 2024 Acme Corp AG — Bern, Switzerland — All rights reserved<br>
    Internal Wiki: <a href="http://wiki.lab.local:3000" style="color:#aaa">wiki.lab.local</a>
    | Mail: <a href="http://mail.lab.local" style="color:#aaa">mail.lab.local</a>
  </footer>
</body>
</html>
EOF

cat > /srv/www/acme/about.html << 'EOF'
<!DOCTYPE html><html><head><title>About — Acme Corp AG</title></head>
<body>
<h1>About Acme Corp AG</h1>
<h2>Leadership</h2>
<ul>
  <li>CEO: Alice Müller (a.mueller@lab.local)</li>
  <li>CTO: Dave Taylor (dtaylor@lab.local)</li>
  <li>CFO: John Smith (jsmith@lab.local)</li>
  <li>IT Manager: Bob Jones (bjones@lab.local)</li>
</ul>
<h2>Infrastructure</h2>
<p>Domain: LAB.LOCAL | AD DC: dc01.lab.local | File Server: fs01.lab.local</p>
<p>Internal Git: git.lab.local | Monitoring: monitor.lab.local</p>
</body></html>
EOF

cat > /srv/www/acme/contact.html << 'EOF'
<!DOCTYPE html><html><head><title>Contact — Acme Corp AG</title></head>
<body>
<h1>Contact</h1>
<p>General: info@acmecorp.lab.local</p>
<p>Support: support@lab.local</p>
<p>Security incidents: security@lab.local | CERT: cert@lab.local</p>
<p>Abuse reports: abuse@lab.local</p>
<p>Postmaster: postmaster@lab.local</p>
</body></html>
EOF

cat > /srv/www/acme/portal.html << 'EOF'
<!DOCTYPE html><html><head><title>Employee Portal</title></head>
<body>
<h1>Acme Corp — Employee Portal</h1>
<p>Please log in via the internal intranet:</p>
<ul>
  <li><a href="http://wiki.lab.local:3000">Internal Wiki / Git (Gitea)</a></li>
  <li><a href="http://monitor.lab.local:9090">Monitoring Dashboard</a></li>
  <li>File Shares: \\FILESERVER\public</li>
  <li>VPN / Remote Access: jump.lab.local (SSH)</li>
</ul>
<p><small>For IT issues contact bjones@lab.local or dtaylor@lab.local</small></p>
</body></html>
EOF

# ── Reload nginx ───────────────────────────────────────────────────────────────
nginx -s reload 2>/dev/null || nginx -g 'daemon off;' &
