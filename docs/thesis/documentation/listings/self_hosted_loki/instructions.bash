ssh ai@10.10.10.20

# https://grafana.com/docs/loki/latest/setup/install/docker/#install-with-docker-compose
mkdir loki
wget https://raw.githubusercontent.com/grafana/loki/v3.7.0/examples/getting-started/docker-compose.yaml -O loki/docker-compose.yaml
wget https://raw.githubusercontent.com/grafana/loki/v3.7.0/examples/getting-started/alloy-local-config.yaml -O loki/alloy-local-config.yaml
wget https://raw.githubusercontent.com/grafana/loki/v3.7.0/examples/getting-started/loki-config.yaml -O loki/loki-config.yaml

# Adjustments needed for rootles podman
systemctl --user enable --now podman.socket

# Adjust the alloy service described in the loki `compose.yaml`
vim loki/docker-compose.yaml

# Add grafana.hiube.ch CNAME entry to ai.hiube.ch
# Add grafana.hiube.ch to linuxserver.io swag config for letsencrypt
vim docker-compose.yaml

# Update nginx conifg
sudo vim swag/nginx/site-confs/default.conf

# Restart services
podman-compose up -d
