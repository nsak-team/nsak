# LangChain WebUI Setup

```bash
# Add nsak.hiube.ch CNAME entry to nsak.hiube.ch
# Add nsak.hiube.ch to linuxserver.io swag config for letsencrypt
vim docker-compose.yaml

# Update nginx conifg
sudo vim swag/nginx/site-confs/default.conf

```


```nginx
server {
    listen 443 ssl;
    # listen 443 quic reuseport;
    listen [::]:443 ssl;
    # listen [::]:443 quic reusepor;

    server_name nsak.hiube.ch;

    include /config/nginx/ssl.conf;

    # Reverse proxy for Drawio
    location / {
        auth_basic "Restricted";
        auth_basic_user_file /config/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

	    proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
