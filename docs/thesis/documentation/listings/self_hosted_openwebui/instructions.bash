ssh ai@10.10.10.20

# Open the nginx defalult.conf and add the contents from lst:open-webui-nginx-conf
vim swag/nginx/site-confs/default.conf

# Start the services
podman-compose up -d
