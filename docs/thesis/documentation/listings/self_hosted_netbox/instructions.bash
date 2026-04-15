ssh ai@10.10.10.20

# https://learn.srlinux.dev/blog/2024/creating-a-network-digital-twin-with-containerlab-and-netbox/
# https://github.com/netbox-community/netbox-docker
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker/

cp docker-compose.override.yml.example docker-compose.override.yml

podman-compose up -d

podman-compose exec netbox /opt/netbox/netbox/manage.py createsuperuser

cd ..

# Add netbox.hiube.ch CNAME entry to ai.hiube.ch
# Add netbox.hiube.ch to linuxserver.io swag config for letsencrypt
vim docker-compose.yaml

# Update nginx conifg
sudo vim swag/nginx/site-confs/default.conf

# Restart services
podman-compose restart swag
