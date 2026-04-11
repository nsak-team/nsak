#!/bin/sh
set -e

# Self-signed TLS certificate
openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
  -keyout /etc/ssl/lab.key \
  -out    /etc/ssl/lab.crt \
  -subj   "/CN=dmz-server.vlab.local"

cat > /etc/nginx/http.d/default.conf << 'EOF'
server {
  listen 80;
  server_name dmz-server.vlab.local 172.16.1.10;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  server_name dmz-server.vlab.local 172.16.1.10;

  ssl_certificate     /etc/ssl/lab.crt;
  ssl_certificate_key /etc/ssl/lab.key;

  location / {
    return 200 'NSAK Enterprise';
    add_header Content-Type text/plain;
  }

  location /secret.txt {
    return 200 "Confidential\n DB Password: {flag:exposed-SOS}";
    add_header Content-Type text/plain;
  }
}
EOF

nginx
echo "[web] nginx started"
