ssh ai@10.10.10.20

# Check nvidia driver is loaded and the GPU was correctly detected, otherwise install the according drivers
nvidia-smi

# Install Ollama and enable systemd service
sudo pacman -Syu ollama
sudo systemctl enable --now ollama
sudo systemctl status ollama

# Download and run a qwen coder 7b model for testing
# Later used models:
# - `qwen2.5:7b-instruct` (tool calling)
# - `gemma4:e2b` (was hyped, but is not that good in tool calling)
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder

# Open the nginx defalult.conf and add the contents from lst:ollama-nginx-conf
vim swag/nginx/site-confs/default.conf

# Start the services, this time they should run successfully.
# For a local setup, certbot will fail to perform the http challenge for issuing the TLS certificate,
# as long as DynDNS and the port forwarding are not set up properly.
podman-compose up -d
