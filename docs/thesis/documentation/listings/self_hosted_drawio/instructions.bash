ssh ai@10.10.10.20

# https://www.drawio.com/blog/diagrams-docker-app
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
