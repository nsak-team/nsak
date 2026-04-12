# Drawio setup

https://www.drawio.com/blog/diagrams-docker-app

```bash
echo "unqualified-search-registries = [\"docker.io\"]" >> /etc/containers/registries.conf

# Add drawio.hiube.ch CNAME entry to ai.hiube.ch
# Add drawio.hiube.ch to linuxserver.io swag config for letsencrypt and add the drawio service from below
vim docker-compose.yaml

# Update nginx conifg
sudo vim swag/nginx/site-confs/default.conf

# Download drawio-mcp
git clone https://github.com/lgazo/drawio-mcp-server.git

# Restart services
podman-compose restart swag
```

```yaml
services:
  # ...

  drawio:
    image: jgraph/drawio
    container_name: drawio
    restart: unless-stopped
    environment:
      - DRAWIO_BASE_URL=https://drawio.hiube.ch
      - DRAWIO_DISABLE_EXTERNAL_PLUGINS=true

  drawio-mcp-server:
    build: ./drawio-mcp-server
    container_name: drawio-mcp-server
    restart: unless-stopped
    command:
      - "node"
      - "packages/drawio-mcp-server/build/index.js"
      - "--transport"
      - "http"
      - "--editor"
      - "--http-port"
      - "3000"

```

```nginx
server {
    listen 443 ssl;
    # listen 443 quic reuseport;
    listen [::]:443 ssl;
    # listen [::]:443 quic reusepor;

    server_name drawio.hiube.ch;

    include /config/nginx/ssl.conf;

    # Reverse proxy for Drawio
    location / {
        auth_basic "Restricted";
        auth_basic_user_file /config/nginx/.htpasswd;

        proxy_pass http://drawio:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

	    proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Reverse proxy for Draw.io MCP server (HTTP transport + built-in editor)
    location /mcp {
        auth_basic "Restricted";
        auth_basic_user_file /config/nginx/.htpasswd;

        proxy_pass http://drawio-mcp-server:3000/mcp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Disable buffering for SSE/streaming
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
        chunked_transfer_encoding on;

        # Required for SSE
        proxy_set_header X-Accel-Buffering no;
    }

    # WebSocket for browser extension
    location /ws {
        auth_basic "Restricted";
        auth_basic_user_file /config/nginx/.htpasswd;

        proxy_pass http://drawio-mcp-server:3333;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
```
