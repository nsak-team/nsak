# Login as ai user
ssh ai@10.10.10.20

# Create a docker compose file and add contents from lst:nginx-docker-compose-yml
vim docker-compose.yml

# Start the services, so that they create the volume mappings etc.
# The containers will most likely fail, but that's fine for now.
podman-compose up -d
podman-compose down
